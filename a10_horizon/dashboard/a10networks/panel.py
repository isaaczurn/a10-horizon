# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import horizon

# from openstack_dashboard.dashboards.project import dashboard
# from a10_horizon.dashboard.a10networks.a10devices import panel as a10devices_panel


# class A10SSLPanel(horizon.Panel):
#     name = _("SSL")
#     slug = "a10ssl"
#     permissions = ("openstack.services.network", )


# class A10LoadBalancingPanel(horizon.Panel):
#     name = _("Load Balancing")
#     slug = "a10loadbalancing"
#     permissions = ('openstack.services.network',)


# class A10ScalingPanel(horizon.Panel):
#     name =_("Scaling LB")
#     slug = "a10scaling"
#     permissions = ("openstack.services.network", )

#     def allowed(self, context):
#         result = False
#         try:
#             import a10_openstack
#             result = True
#         except ImportError as ex:
#             LOG.error("a10_openstack must be installed to use this panel.")
#             LOG.exception(ex)
#         return result


network_config = (
    getattr(settings, 'OPENSTACK_NEUTRON_NETWORK', {}) or
    getattr(settings, 'OPENSTACK_QUANTUM_NETWORK', {})
)

# if network_config.get('enable_lb'):
#     dashboard.Project.register(A10NetworksPanel)
