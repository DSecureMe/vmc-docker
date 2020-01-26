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
from unittest import mock
from elasticsearch_dsl import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vmc.config.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from datetime import datetime, timedelta
from vmc.ralph.tasks import load_all_assets
from vmc.knowledge_base.tasks import update_cve_cwe, update_cve, update_cwe, START_YEAR
from vmc.assets.documents import AssetDocument
from vmc.vulnerabilities.documents import VulnerabilityDocument
from vmc.knowledge_base.documents import CveDocument


def main():
    load_all_assets()

    update_cwe()

    update_cve(random.randint(START_YEAR, datetime.now().year + 1))

    print('Creating 2000 vulnerabilities')
    query = Q({'function_score': {
        "query": {"match_all": {}},
        "boost": "5",
        "random_score": {},
        "boost_mode": "multiply"
    }})

    for idx in range(1, 2000):
        cve_search = CveDocument.search().query(query)[1]
        cve = cve_search.execute().hits[0]
        as_search = AssetDocument.search().query(query)[1]
        asset = as_search.execute().hits[0]
        with mock.patch('vmc.common.elastic.documents.now') as mock_now:
            mock_now.return_value = datetime.now() - timedelta(days=random.randint(1, 90))
            VulnerabilityDocument(
                asset=asset,
                cve=cve,
                description=cve.summary,
                solution='SAMPLE SOLUTION {}'.format(idx),
                exploit_available=random.choices([True, False])[0],
                port=random.randint(1, 1024),
                svc_name='service {}'.format(idx),
                protocol='tcp'
            ).save(refresh=True)

    update_cve_cwe.delay()

    print('Done')


if __name__ == '__main__':
    main()
