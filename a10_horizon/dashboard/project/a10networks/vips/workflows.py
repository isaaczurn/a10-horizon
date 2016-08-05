# Copyright (C) 2016-2016, A10 Networks Inc. All rights reserved.
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

# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.

import logging

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import workflows

# a10_horizon.dashboard.api.client.Client extends neutron.api.client.Client
# from a10_horizon.dashboard.api import lbaasv2 as lbaasv2_api


LOG = logging.getLogger(__name__)


class CreateVipAction(workflows.Action):
    name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    description = forms.CharField(label=_("Description"), min_length=1,
                                  max_length=255, required=False)

    class Meta(object):
        name = _("Create VIP")
        # TODO(mdurrant) - Add a10-specific permissions
        permissions = ("openstack.services.network", )
        help_text = _("Specify the details for the VIP below")


class CreateVipStep(workflows.Step):
    action_class = CreateVipAction
    contributes = ("name", "description")


class CreateVipWorkflow(workflows.Workflow):
    slug = "addvip"
    name = _("Create VIP")
    default_steps = (CreateVipStep, )
    success_url = "horizon:project:a10vips:index"
    finalize_button_name = "Create VIP"

    def handle(self, request, context):
        success = True
        try:
            pass
        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Create VIP"))
        return success
