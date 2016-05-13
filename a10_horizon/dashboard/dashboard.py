# Copyright 2016,  A10 Networks
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

# from django.conf import settings
# from django.utils.translation import ugettext_lazy as _
# import horizon

# from openstack_dashboard.dashboards.project import dashboard

# from a10_horizon.dashboard.a10networks import panel as a10networks_panel


# network_config = (
#     getattr(settings, 'OPENSTACK_NEUTRON_NETWORK', {}) or
#     getattr(settings, 'OPENSTACK_QUANTUM_NETWORK', {})
# )

# class A10NetworksDashboard(horizon.Dashboard):
#     name = _("A10 Networks")
#     slug = "a10networkspanelgroup"
#     panels = (a10networks_panel.A10PanelGroup.panels)

# # dashboard.register(A10NetworksDashboard)

# if network_config.get('enable_lb'):
#     dashboard.Project.register(a10networks_panel.A10NetworksPanel)
#     project_dashboard = horizon.get_dashboard("project")
#     import pdb; pdb.set_trace()
#     network_panelgroup = project_dashboard.get_panel_group("network")
#     network_panelgroup.panels.append("a10networks")
