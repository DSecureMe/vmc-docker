"""
 * Licensed to DSecure.me under one or more contributor
 * license agreements. See the NOTICE file distributed with
 * this work for additional information regarding copyright
 * ownership. DSecure.me licenses this file to you under
 * the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
"""
import os
import random
import time
import concurrent.futures

from unittest import mock

from celery import group
from elasticsearch_dsl import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vmc.config.settings")

from django.core.wsgi import get_wsgi_application
from elasticsearch_dsl.connections import get_connection
from elasticsearch.helpers import bulk

application = get_wsgi_application()
from vmc.ralph.tasks import start_update_assets
from datetime import datetime, timedelta
from vmc.ralph.models import Config as RalphConfig
from vmc.ralph.tasks import _update_assets
from vmc.knowledge_base.tasks import update_cwe, update_cve, START_YEAR, update_exploits
from vmc.assets.documents import AssetDocument
from vmc.vulnerabilities.documents import VulnerabilityDocument
from vmc.knowledge_base.documents import CveDocument
from vmc.processing.tasks import start_processing

OS_FAMILY = {
    'Redhat': ['Redhat 5', 'Redhat 6', 'Redhat 7'],
    'Debian': ['Debian 8', 'Debian 9', 'Debian 10'],
    'Windows': ['Windows Server 2012', 'Windows Server 2016', 'Windows Server 2019'],
    'IBM': ['IBM AIX 5', 'IBM AIX 6', 'IBM AIX 7']
}

CPE_LIST = {
    'Redhat 5': 'enterprise_linux_server:5',
    'Redhat 6': 'enterprise_linux_server:6',
    'Redhat 7': 'enterprise_linux_server:7',
    'Debian 8': 'debian_linux:8',
    'Debian 9': 'debian_linux:9',
    'Debian 10': 'debian_linux:10',
    'Windows Server 2012': 'windows_server_2012',
    'Windows Server 2016': 'windows_server_2016',
    'Windows Server 2019': 'windows_server_2019',
    'IBM AIX 5': 'aix:5',
    'IBM AIX 6': 'aix:6',
    'IBM AIX 7': 'aix:7',
    }

RAND_QUERY = Q({'function_score': {
    "query": {"match_all": {}},
    "boost": "5",
    "random_score": {},
    "boost_mode": "multiply"
}})


def _bulk(docs):
    bulk(get_connection(), docs, index=VulnerabilityDocument.Index.name)


def get_cve_sets(asset_count):
    cve_sets = {name: set() for name in CPE_LIST.keys()}
    cve_cvss_3 = CveDocument.search().filter('exists', field='base_score_v3')
    cve_cvss_2 = CveDocument.search()
    cve_count = 0

    while cve_count < asset_count * 4:
        cve_count = 0
        for os in CPE_LIST:
            max_cve = cve_cvss_3.filter('wildcard', cpe__name=F'*{CPE_LIST[os]}*').query(RAND_QUERY).count()
            count = random.randint(1, max_cve)

            if max_cve > 0:
                cves = cve_cvss_3.filter('wildcard', cpe__name=F'*{CPE_LIST[os]}*').query(RAND_QUERY)[0:count]

            else:
                cves = cve_cvss_2.filter('wildcard', cpe__name=F'*{CPE_LIST[os]}*').query(RAND_QUERY)[0:count]

            cve_sets[os].update(cve for cve in cves)

        for cve in cve_sets:
            cve_count += len(cve_sets[cve])

        print(F'The amount of cve drawn: {cve_count}, '
              F'assets count: {asset_count}, '
              F'ratio: {round(cve_count / asset_count, 2)}')

    for os_name in cve_sets:
        print(F'System name: {os_name}, cve pool count: {len(cve_sets[os_name])}')

    return {k: list(v) for k, v in cve_sets.items()}


def generate_vulns(asset_count, asset_search, cve_sets):
    bulk_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    bulk_pool, vulns, assets = [], [], []
    asset_vuln = {}
    vuln_count = 0
    step = 10

    for a in asset_search.scan():
        asset_vuln[a.ip_address] = []
        assets.append(a)

    while vuln_count / asset_count < 130:
        vuln_count = 0

        if len(assets) == 0:
            break

        for asset in assets:
            cve_set = cve_sets[asset.os]

            if len(cve_sets[asset.os]) == len(asset_vuln[asset.ip_address]):
                assets.remove(asset)
                break

            cve = random.choice(cve_set)
            if cve.id not in asset_vuln[asset.ip_address]:
                asset_vuln[asset.ip_address].append(cve)
                with mock.patch('vmc.elasticsearch.documents.now') as mock_now:
                    mock_now.return_value = datetime.now() - timedelta(days=random.randint(1, 90))
                    vulns.append(VulnerabilityDocument(
                        id=F'{asset.id}-{cve.id}',
                        asset=asset,
                        cve=cve,
                        description=cve.summary,
                        protocol='tcp'
                    ).to_dict())

        if len(vulns) > 10000:
            bulk_pool.append(bulk_executor.submit(_bulk, vulns))
            vulns = []

        for ip in asset_vuln:
            vuln_count += len(asset_vuln[ip])

        if vuln_count / asset_count > step:
            print(F'Generated vulns: {vuln_count}, '
                  F'assets count: {asset_count}, '
                  F'ratio: {round(vuln_count / asset_count, 2)}')
            step += 10

    if vulns:
        bulk_pool.append(bulk_executor.submit(_bulk, vulns))

    concurrent.futures.wait(bulk_pool)

    print(F'Generated vulns: {vuln_count}, '
          F'assets count: {asset_count}, '
          F'ratio: {round(vuln_count / asset_count, 2)}')


def main():
    start_update_assets()
    #start_processing()
    #print('Download CVEs')
    """
    group(
        update_cwe.si() |
        group(update_cve.si(year) for year in range(START_YEAR, datetime.now().year + 1)) |
        update_exploits.si()
    )().get()

    print('Update Assets')
    _update_assets(RalphConfig.objects.first().pk)


    asset_search = AssetDocument.search()

    times = 0
    while asset_search.count() == 0:
        print('Assets count still 0, waiting...')
        time.sleep(1)
        if times > 4:
            print('Unable to count assets, exiting...')
            exit(1)

        times += 1

    asset_count = asset_search.count()

    # Draw enough unique CVEs to make them min 4 times more than there are hosts
    cve_sets = get_cve_sets(asset_count)

    # draw as many as there will be 130 on average per host
    generate_vulns(asset_count, asset_search, cve_sets)

    start_processing()
    """


if __name__ == '__main__':
    main()
