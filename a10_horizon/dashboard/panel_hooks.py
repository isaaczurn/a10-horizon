# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.

# Add "A10 Networks" to "Network" panelgroup
from django.conf import settings

import horizon

from openstack_dashboard.dashboards.project import dashboard

from a10_horizon.dashboard.a10networks.panel import A10NetworksPanel

network_config = (
    getattr(settings, 'OPENSTACK_NEUTRON_NETWORK', {}) or
    getattr(settings, 'OPENSTACK_QUANTUM_NETWORK', {})
)

if network_config.get('enable_lb'):
    dashboard.Project.register(A10NetworksPanel)
    project_dashboard = horizon.get_dashboard("project")
    network_panelgroup = project_dashboard.get_panel_group("network")
    network_panelgroup.panels.append("a10networks")
