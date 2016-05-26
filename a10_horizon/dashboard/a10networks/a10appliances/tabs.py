# Copyright 2015,  A10 Networks
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

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

import a10_horizon.dashboard.a10networks.a10appliances.tables as p_tables
import a10_horizon.dashboard.api.a10devices as a10api


class A10AppliancesTab(tabs.TableTab):
    table_classes = (p_tables.A10ApplianceTable,)
    name = _("A10 Appliances")
    slug = "a10appliancestab"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_a10appliancestable_data(self):
        result = []

        try:
            result = a10api.get_a10_appliances(self.request)
        except Exception:
            result = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve appliance list.'))
        return result


class A10DeviceInstanceTab(tabs.TableTab):
    table_classes = (p_tables.A10DeviceInstanceTable,)
    name = "a10deviceinstancestab"


class A10Tabs(tabs.TabGroup):
    slug = "a10tabs"
    tabs = (A10AppliancesTab, )
    sticky = True
