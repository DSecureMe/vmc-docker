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
import ralph.settings

ralph.settings.CHECK_IP_HOSTNAME_ON_SAVE = False
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ralph.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from ralph.assets.models import Asset, Ethernet
from ralph.networks.models.networks import IPAddress

USED_IPS = []
USED_MAC = []


def _generate_mac():
    while True:
        mac = "52:54:00:%02x:%02x:%02x" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        if mac not in USED_MAC:
            USED_MAC.append(mac)
            return mac


def _random_ip_address():
    while True:
        octets = []
        for x in range(4):
            octets.append(str(random.randint(0, 255)))
        ip = '.'.join(octets)
        if ip not in USED_IPS:
            USED_IPS.append(ip)
            return ip


def main():
    used_ips = []
    dc_assets = Asset.objects.filter(backofficeasset__isnull=True)
    print('Generating IP addesses for', dc_assets.count())

    for idx, asset in enumerate(dc_assets):
        ip = _random_ip_address()
        used_ips.append(ip)
        eth = Ethernet.objects.create(base_object=asset, mac=_generate_mac())
        IPAddress.objects.create(address=_random_ip_address(), ethernet=eth, hostname=asset.hostname)

    print('Generation done')


if __name__ == '__main__':
    main()
