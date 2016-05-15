# Copyright (C) 2016, A10 Networks Inc. All rights reserved.
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
# import pdb; pdb.set_trace()
from openstack_dashboard.local import local_settings
import a10_horizon


# The slug of the panel group to be added to HORIZON_CONFIG. Required.
PANEL_GROUP = 'a10networks'
# The display name of the PANEL_GROUP. Required.
PANEL_GROUP_NAME = _('A10 Networks')
# The slug of the dashboard the PANEL_GROUP associated with. Required.
PANEL_GROUP_DASHBOARD = 'project'
AUTO_DISCOVER_STATIC_FILES = True

# template_dirs = getattr(local_settings, "TEMPLATE_DIRS", [])
# template_dirs.append("{0}/{1}/{2}".format(a10_horizon.__path__[0], "dashboard/a10ssl", "templates"))
# local_settings.TEMPLATE_DIRS = template_dirs


#                       'a10_horizon.dashboard.a10networks.a10scaling',
#                       'a10_horizon.dashboard.a10networks.a10devices']
