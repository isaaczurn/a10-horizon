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

import logging
import uuid

from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
import horizon.forms as forms
import horizon.tables as tables
import horizon.workflows as workflows

from openstack_dashboard import api as os_api
import openstack_dashboard.api.glance as glance_api
import openstack_dashboard.api.neutron as neutron_api
import openstack_dashboard.api.nova as nova_api
from openstack_dashboard.dashboards.project.instances import utils as instance_utils

from a10_horizon.dashboard.api import deviceinstances as api

import instance_helpers


GLANCE_API_VERSION_LIST = 2
GLANCE_API_VERSION_CREATE = 2
GLANCE_API_VERSION_UPDATE = 1

LOG = logging.getLogger(__name__)


class SetInstanceDetailsAction(workflows.Action):
    name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    mgmt_network = forms.ChoiceField(label=_("Management Network"),
                                     required=True)
    data_networks = forms.MultipleChoiceField(
        label=_("Data Networks"),
        widget=forms.ThemableCheckboxSelectMultiple(),
        error_messages={
            'required': _('At least one data network must be specified')
        },
        help_text=_("Launch a vThunder instance with the specified networks"))

    # Dynamic population of network choices.
    def __init__(self, request, *args, **kwargs):
        super(SetInstanceDetailsAction, self).__init__(request, *args, **kwargs)

    def populate_mgmt_network_choices(self, request, context):
        return instance_utils.network_field_data(request)

    def populate_data_networks_choices(self, request, context):
        return instance_utils.network_field_data(request)


    class Meta(object):
        name = _("Create New vThunder Instance")
        # TODO(mdurrant) - Add a10-specific permissions
        permissions = ("openstack.services.network", )
        help_text = _("Specify the details for your instance below")


class AddDeviceInstanceStep(workflows.Step):
    action_class = SetInstanceDetailsAction
    # image name, mgmt network, member network, vip network
    contributes = ("name", "mgmt_network", "data_networks")


class AddDeviceInstanceWorkflow(workflows.Workflow):
    slug = "adddeviceinstance"
    name = _("Add vThunder Instance")
    default_steps = (AddDeviceInstanceStep, )

    success_url = "horizon:project:a10instances:index"
    finalize_button_name = "Create vThunder Instance"

    def handle(self, request, context):
        # Create the instance manager, giving it the context so it knows how to auth
        auth_url = instance_helpers.url_for(request)
        config = {
            "keystone_version": 2,
            "keystone_auth_url": auth_url,
            "nova_api_version": "2.1",
            'username': 'admin',
            'password': 'a10',
            "glance_image": "acos4.1.1",
            "nova_flavor": "vthunder.small",
        }

        try:
            import pdb; pdb.set_trace()
            context["image"] ='acos4.1.1'
            context["flavor"] = "vthunder.small"
            context["networks"] = [context["mgmt_network"]]
            for x in context["data_networks"]:
                context["networks"].append(x)

            instance_mgr = instance_helpers.instance_manager_from_context(config, request)
            instance_data = instance_mgr.create_instance(context)
            LOG.debug("Instance: {0}".format(instance_data))

        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to create instance due to external error."))
            # Abort!
            return False

        try:
            remove_keys = ["image", "data_networks", "mgmt_network", "flavor", "networks"]
            api.create_a10_device_instance(request, **context)
        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to create device instance."))
        return redirect(self.success_url)
