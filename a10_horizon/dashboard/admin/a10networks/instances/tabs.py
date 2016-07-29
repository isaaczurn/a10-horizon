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

import tables as p_tables
import a10_horizon.dashboard.api.deviceinstances as a10api
import helper

class DeviceInstanceAdminTableTab(tabs.TableTab):
    table_classes = (p_tables.DeviceInstanceAdminTable,)
    name = _("LB Device Instances")
    slug = "deviceinstanceadmin_tab"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_deviceinstanceadmintable_data(self):
        result = []
        try:
            result = a10api.get_a10_device_instances(self.request)
            result = helper.get_result(self.request, result)
        except Exception:
            result = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve appliance list.'))
        return result


class DeviceInstanceAdminTabs(tabs.TabGroup):
    slug = "instancetabs"
    template_name = "horizon/common/_tab_group.html"
    sticky = False
    show_single_tab = True
    tabs = (DeviceInstanceAdminTableTab,)


class DeviceInstanceTabView(tabs.TabView):
    tab_group_class = DeviceInstanceAdminTabs
    template_name = "horizon/common/_detail.html"
