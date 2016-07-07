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

import a10_horizon.dashboard.project.a10networks.instances.tables as p_tables
import a10_horizon.dashboard.api.a10devices as a10api


class OverviewTabs(tabs.TabGroup):
    slug = "overviewtabs"
    template_name = "horizon/common/_tab_group.html"
    sticky = False
    show_single_tab = False
