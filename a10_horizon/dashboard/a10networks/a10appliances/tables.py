# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

# from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables


LOG = logging.getLogger(__name__)


class A10ApplianceTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    name = tables.Column("name", verbose_name=_("Hostname"), hidden=False)
    ip = tables.Column("host", verbose_name="Management IP")
    api_ver = tables.Column("api_version", verbose_name="API Version")
    nova_instance_id = tables.Column("nova_instance_id", hidden=True)

    class Meta(object):
        name = "a10appliancestable"
        verbose_name = _("A10 Appliances")
        table_actions = ()
        row_actions = ()


class A10DeviceInstanceTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    tenant_id = tables.Column("tenant_id", verbose_name=_("Tenant ID"), hidden=True)
    ip_address = tables.Column("ip_address", verbose_name=_("IP Address"), hidden=True)
    nova_instance_id = tables.Column("nova_instance_id", verbose_name=_("Nova Instance ID"),
                                     hidden=True)

    class Meta(object):
        name = "a10deviceinstancetable"
        verbose_name = "a10deviceinstancetable"
        table_actions = ()
        row_actions = ()
