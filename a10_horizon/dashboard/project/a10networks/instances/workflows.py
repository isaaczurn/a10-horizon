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

from django.utils.translation import ugettext_lazy as _

import horizon.forms as forms
import horizon.tables as tables
import horizon.workflows as workflows
from openstack_dashboard import api as os_api
import openstack_dashboard.api.glance as glance_api
import openstack_dashboard.api.neutron as neutron_api
import openstack_dashboard.api.nova as nova_api
from openstack_dashboard.dashboards.project.instances import utils as instance_utils

from a10_horizon.dashboard.api import deviceinstances as api


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
        super(AddPolicyAction, self).__init__(request, *args, **kwargs)

        # this populates the dropdowns that allow the user to connect
        # management network and other networks as needed.
        # networks = []

        # tenant_id = request.user.tenant_id
        # is_admin = request.user.is_admin

        # # names of form fields representing vThunder interfaces.
        # interfaces = ["mgmt_network", "vip_network", "member_network"]
        # interface_choices = {}

        # mgmt_network_choices = [('', _("Select the management network."))]

        # try:
        #     if not is_admin:
        #         kwargs["tenant_id"] = tenant_id
        #     networks = neutron_api.network_list(request, **kwargs)

        # except Exception as ex:
        #     LOG.exception(ex)
        #     exceptions.handle(request, _("Error retrieving networks from neutron."))

        # for i in interfaces:
        #     interface_choices[i] = []
        #     for net in networks:
        #         interface_choices[i].append((net.id, net.name))

        # for x in interfaces:
        #     self.fields[x] = interface_choices[x]

    # def clean(self):
    #     super(SetInstanceDetailsAction, self).clean()
    #     # Validate networks here.

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
    success_url = "a10networks:instances:index"
    finalize_button_name = "Create vThunder Instance"

    def handle(self, request, context):
        try:
            api.create_a10_device_instance(request, **context)
        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to delete scaling action"))
        return redirect(self.success_url)
