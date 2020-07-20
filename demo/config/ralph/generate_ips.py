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

from django.contrib.auth import get_user_model
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.contenttypes.models import ContentType
from ralph.assets.models import Ethernet
from ralph.data_center.models import DataCenterAsset
from ralph.networks.models import IPAddress
from ralph.lib.custom_fields.models import CustomFieldValue, CustomField, CustomFieldTypes

USED_IPS = []
USED_MAC = []

IMPACT = ['LOW', 'MEDIUM', 'HIGH', 'NOT_DEFINED']
IMPACT_WEIGHTS = [0.25, 0.25, 0.25, 0.25]

OS_FAMILY = {
    'Redhat': ['Redhat 5', 'Redhat 6', 'Redhat 7'],
    'Debian': ['Debian 8', 'Debian 9', 'Debian 10'],
    'Windows': ['Windows Server 2012', 'Windows Server 2016', 'Windows Server 2019'],
    'IBM': ['IBM AIX 5', 'IBM AIX 6', 'IBM AIX 7']
}

"""
Probability distribution of the images used modeled on:
https://ieeexplore.ieee.org/abstract/document/6195556
"""
OS_FAMILY_WEIGHTS = [0.53, 0.07, 0.25, 0.15]

USER_MODEL = get_user_model()
MIN_IP_COUNT = 1000


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
        octets = ['192', '168']
        for x in range(2):
            octets.append(str(random.randint(1, 254)))
        ip = '.'.join(octets)
        if ip not in USED_IPS:
            USED_IPS.append(ip)
            return ip


def main():
    dc_assets = DataCenterAsset.objects.all()

    os_field = CustomField.objects.create(
        name='os',
        type=CustomFieldTypes.STRING
    )
    confidentiality_field = CustomField.objects.create(
        name='confidentiality',
        type=CustomFieldTypes.CHOICE,
        choices='LOW|MEDIUM|HIGH|NOT_DEFINED',
    )
    integrity_field = CustomField.objects.create(
        name='integrity',
        type=CustomFieldTypes.CHOICE,
        choices='LOW|MEDIUM|HIGH|NOT_DEFINED',
    )
    availability_field = CustomField.objects.create(
        name='availability',
        type=CustomFieldTypes.CHOICE,
        choices='LOW|MEDIUM|HIGH|NOT_DEFINED',
    )
    content_type = ContentType.objects.get_for_model(DataCenterAsset)

    print('Generating random data for addesses', dc_assets.count())
    for idx, asset in enumerate(dc_assets):
        asset.custom_fields.add(CustomFieldValue.objects.create(
            custom_field=confidentiality_field,
            value=random.choices(IMPACT, IMPACT_WEIGHTS)[0],
            object_id=asset.pk,
            content_type=content_type
        ))
        asset.custom_fields.add(CustomFieldValue.objects.create(
            custom_field=integrity_field,
            value=random.choices(IMPACT, IMPACT_WEIGHTS)[0],
            object_id=asset.pk,
            content_type=content_type
        ))
        asset.custom_fields.add(CustomFieldValue.objects.create(
            custom_field=availability_field,
            value=random.choices(IMPACT, IMPACT_WEIGHTS)[0],
            object_id=asset.pk,
            content_type=content_type
        ))
        os_family = random.choices(list(OS_FAMILY.keys()), OS_FAMILY_WEIGHTS)[0]
        asset.custom_fields.add(CustomFieldValue.objects.create(
            custom_field=os_field,
            value=random.choices(OS_FAMILY[os_family])[0],
            object_id=asset.pk,
            content_type=content_type
        ))

        if random.random() > 0.90 and not asset.service_env.service.business_owners.exists():
            bo = USER_MODEL.objects.order_by('?').first()
            asset.service_env.service.business_owners.add(bo)

        if random.random() > 0.90 and not asset.service_env.service.technical_owners.exists():
            bo = USER_MODEL.objects.order_by('?').first()
            asset.service_env.service.technical_owners.add(bo)

        asset.save()

    while len(USED_IPS) <= MIN_IP_COUNT:
        for idx, asset in enumerate(dc_assets):
            eth = Ethernet.objects.create(base_object=asset.asset, mac=_generate_mac())
            IPAddress.objects.create(address=_random_ip_address(), ethernet=eth, hostname=asset.hostname)
        if len(USED_IPS) // 100:
            print(len(USED_IPS))

    print(F'Generated ips: {len(USED_IPS)}')
    print('Generation done')


if __name__ == '__main__':
    main()
