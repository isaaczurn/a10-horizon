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
import a10_horizon.dashboard.api.a10devices as a10api


class OverviewAdminTableTab(tabs.TableTab):
    table_classes = (p_tables.OverviewAdminTable,)
    name = _("SLB Overview")
    slug = "overviewadmintable"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_overviewadmintable_data(self):
        try:
            rv = []
            # Return all VIPs, ordered by tenant.
        except Exception as ex:
            rv = []
            LOG.exception(ex)
            errmsg = _("Unable to retrieve VIP list")
            exceptions.handle(self.tab_group.request, errmsg)

        return rv


class OverviewTopologyAdminTab(tabs.Tab):
    name = _("SLB Topology")
    slug = "overtopologyadmin_tab"
    template_name = "horizon/common/_detail.html"


class OverviewAdminTabs(tabs.TabGroup):
    slug = "overviewadmintabs"
    template_name = "horizon/common/_tab_group.html"
    sticky = False
    show_single_tab = True
    tabs = (OverviewAdminTableTab, OverviewTopologyAdminTab)


class OverviewAdminTabView(tabs.TabView):
    tab_group_class = OverviewAdminTabs
