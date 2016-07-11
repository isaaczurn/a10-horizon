# Copyright 2015 A10 Networks
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

from horizon import tabs
from horizon import workflows

import tabs as p_tabs
import workflows as p_workflows

import a10_horizon.dashboard.api.deviceinstances as a10api


class IndexView(tabs.TabbedTableView):
    tab_group_class = p_tabs.A10Tabs
    template_name = "instances/_tabs.html"

    def post(self, request, *args, **kwargs):
        obj_ids = request.POST.getlist('object_ids')
        action = request.POST['action']
        m = re.search('.delete([a-z]+)', action).group(1)
        if obj_ids == []:
            obj_ids.append(re.search('([0-9a-z-]+)$', action).group(1))

        delete_action = a10api.delete_a10_appliance
        for obj_id in obj_ids:
            success_msg = "Deleted {0} {1}".format("Instance", obj_id)
            failure_msg = "Unable to delete {0} {1}".format("Instance", obj_id)

            try:
                delete_action(request, obj_id)
                messages.success(request, success_msg)
            except Exception as ex:
                exceptions.handle(request, failure_msg)
                LOG.exception(ex)

        return self.get(request, *args, **kwargs)
