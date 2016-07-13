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
# import a10_horizon.dashboard.api.vips as a10api


TABLE_TEMPLATE = "horizon/common/_detail_table.html"
DEFAULT_TEMPLATE = "horizon/common/_detail.html"


class VipsTab(tabs.TableTab):
    table_classes = (p_tables.VipTable,)
    name = _("VIPs")
    slug = "a10vipstab"
    template_name = TABLE_TEMPLATE
    preload = False

    def get_viptable_data(self):
        result = []

        try:
            result = a10api.get_a10_appliances(self.request)
        except Exception:
            result = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve appliance list.'))
        return result


class VipTabs(tabs.TabGroup):
    slug = "a10tabs"
    tabs = (VipsTab, )
    sticky = False
    show_single_tab = True
