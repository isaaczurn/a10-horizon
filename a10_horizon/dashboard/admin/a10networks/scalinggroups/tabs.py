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

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

import tables as p_tables
import a10_horizon.dashboard.api.scaling as a10api


class ScalingGroupAdminTableTab(tabs.TableTab):
    table_classes = (p_tables.ScalingGroupAdminTable,)
    name = _("Scaling Groups")
    slug = "scalinggroupadmintable"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_scalinggroupadmintable_data(self):
        try:
            rv = a10api.get_a10_scaling_groups(self.tab_group.request)
            # Return all VIPs, ordered by tenant.
        except Exception as ex:
            rv = []
            LOG.exception(ex)
            errmsg = _("Unable to retrieve scaling group list")
            exceptions.handle(self.tab_group.request, errmsg)

        return rv


class ScalingGroupAdminTabs(tabs.TabGroup):
    slug = "scalinggroupadmintabs"
    template_name = "horizon/common/_tab_group.html"
    sticky = False
    show_single_tab = True
    tabs = (ScalingGroupAdminTableTab, )


class ScalingGroupTabView(tabs.TabView):
    tab_group_class = ScalingGroupAdminTabs
