# Copyright (C) 2016, A10 Networks Inc. All rights reserved.
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

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from horizon import messages
from horizon import tabs
from horizon import views
from horizon import workflows
import logging
import re

import a10_horizon.dashboard.api.deviceinstances as a10api
import workflows as a_workflows
import forms as p_forms
import tabs as p_tabs
from openstack_dashboard.api import nova as nova_api


LOG = logging.getLogger(__name__)


class IndexView(tabs.TabView):
    template_name = "instances/_tabs.html"
    tab_group_class = p_tabs.DeviceInstanceAdminTabs
    page_title = ""


    def post(self, request, *args, **kwargs):
        obj_ids = request.POST.getlist('object_ids')
        action = request.POST['action']

        # m = re.search('.delete([a-z]+)', action).group(1)
        if obj_ids == []:
            obj_ids.append(re.search('([0-9a-z-]+)$', action).group(1))

        delete_action = a10api.delete_a10_device_instance
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


class MigrateDeviceView(forms.views.ModalFormView):
    name = _("Migrate Device")
    form_class = p_forms.MigrateDevice
    success_url = reverse_lazy("horizon:admin:a10deviceinstances:index")
    template_name = "instances/migrate_device.html"
    submit_url = None

    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        pass

    def get_context_data(self, **kwargs):
        context = super(MigrateDeviceView, self).get_context_data(**kwargs)
        import pdb; pdb.set_trace()
        context["nova_instance_id"] = self.kwargs["id"]
        return context
