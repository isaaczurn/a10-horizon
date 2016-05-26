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

import a10_neutron_lbaas.a10_config as a10_config
import a10_horizon.dashboard.api.base as base
import a10_neutron_lbaas.vthunder.instance_manager as im


import horizon.forms as forms
import horizon.tables as tables
import horizon.workflows as workflows
import openstack_dashboard.api.glance as glance_api
import openstack_dashboard.api.neutron as neutron_api
import openstack_dashboard.api.nova as nova_api


GLANCE_API_VERSION_LIST = 2
GLANCE_API_VERSION_CREATE = 2
GLANCE_API_VERSION_UPDATE = 1

LOG = logging.getLogger(__name__)

def instance_manager_for(request):
    return im.InstanceManager(
        base.project_id_for(request),
        session=base.session_for(request))


class AddApplianceAction(workflows.Action):
    name = forms.CharField(max_length=255, label=_("Name"))

    flavor = forms.ChoiceField(label=_("Flavor"))
    image = forms.ChoiceField(label=_("Image"))
    # TODO(mdurrant): mgmt network/dp network/vip network
    networks = forms.ChoiceField(label=_("Networks"))

    def __init__(self, request, *args, **kwargs):
        super(AddApplianceAction, self).__init__(request, *args, **kwargs)
        # So we can get networks for the tenant
        tenant_id = request.user.tenant_id

        image_filter = {
            "tag": ["a10"]
        }

        # default values
        network_choices = [((""), _("Select a network"))]
        flavor_choices = [((""), _("Select a flavor"))]
        image_choices = [((""), _("Select an image"))]

        # Get our data from the API
        networks = neutron_api.network_list_for_tenant(request, tenant_id=tenant_id)
        flavors = nova_api.flavor_list(request)

        images = glance_api.glanceclient(request,
                                         version=GLANCE_API_VERSION_LIST
                                         ).images.list()

        # Build the list from IDs/names
        self._build_choices_list(network_choices, networks)
        self._build_choices_list(flavor_choices, flavors)
        self._build_choices_list(image_choices, list(images))

        # assign it to the choices
        self.fields["networks"].choices = network_choices
        self.fields["flavor"].choices = flavor_choices
        self.fields["image"].choices = image_choices

    class Meta(object):
        name = _("Add Appliance")
        permissions = ('openstack.services.network',)
        help_text_template = '_create_appliance_help.html'

    def _build_choices_list(self, target=[], choices=[], transform=lambda x: ((x.id, x.name))):
        for x in choices:
            target.append(transform(x))


class AddApplianceStep(workflows.Step):
    action_class = AddApplianceAction
    contributes = ("name", "flavor", "image", "networks")

    def contribute(self, data, context):
        context = super(AddApplianceStep, self).contribute(data, context)
        if data:
            networks = context["networks"]
            context["networks"] = [networks]
            return context


class AddAppliance(workflows.Workflow):
    slug = "addappliance"
    name = _("Add Appliance")
    finalize_button_name = _("Add")
    success_message = _('Added appliance "%s".')
    failure_message = _('Unable to add appliance "%s".')
    success_url = "horizon:project:a10appliances:index"
    default_steps = (AddApplianceStep,)

    def format_status_message(self, message):
        name = self.context.get('name')
        return message % name

    def handle(self, request, context):
        # Create the instance manager, giving it the context so it knows how to auth
        instance_mgr = instance_manager_for(request)
        instance_data = instance_mgr.create_instance(context)

        LOG.debug("Instance: {0}".format(instance_data))
        return True


class DeleteApplianceAction(tables.Action):
    name = "deleteappliance"
    verbose_name = _("Delete Appliance")
    # url = "horizon:project:a10appliances:deleteappliance"
    # icon = "minus"
    # classes = ("ajax-modal", )

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Appliance",
            u"Delete A10 Appliances",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of A10 Appliance",
            u"Scheduled deletion of A10 Appliances",
            count
        )

    def handle(self, data_table, request, object_ids):
        for obj_id in object_ids:
            instance_id = data_table.get_object_by_id(obj_id)["nova_instance_id"]
            appliance_id = obj_id
            a10api.delete_a10_appliance(request, obj_id)
            imgr = instance_manager_for(request)
            imgr.delete_instance(instance_id)
            # super(DeleteApplianceAction, self).handle(data_table, request, object_ids)


