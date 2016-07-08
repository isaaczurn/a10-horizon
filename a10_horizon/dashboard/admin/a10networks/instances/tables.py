# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.
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
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables


LOG = logging.getLogger(__name__)


class DeviceInstanceAdminTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    name = tables.Column("name", verbose_name=_("Hostname"), hidden=False, link=get_instance_detail)
    ip = tables.Column("host", verbose_name="Management IP")
    api_ver = tables.Column("api_version", verbose_name="API Version")
    nova_instance_id = tables.Column("nova_instance_id", hidden=False, link=get_instance_detail)

    class Meta(object):
        name = "deviceinstanceadmintable"
        verbose_name = _("Device Instances")
        table_actions = ()
        row_actions = ()

    def get_a10admindeviceinstancetable_data(self):
        return []
