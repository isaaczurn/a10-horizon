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
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import workflows

from neutron_lbaas_dashboard.api import lbaasv2
# Yeah, instances in networking - easy way to get subnet data.
from openstack_dashboard.api import neutron as neutron_api
from openstack_dashboard.dashboards.project.instances import utils as instance_utils


LOG = logging.getLogger(__name__)

"""
Notes:

v2 defines a VIP as a combination of a listener/loadbalancer.

"""


class CreateLbAction(workflows.Action):
    lb_name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    lb_description = forms.CharField(label=_("Description"), min_length=1,
                                  max_length=255, required=False)
    vip_subnet = forms.ChoiceField(label=_("VIP Subnet"), required=True)

    def populate_vip_subnet_choices(self, request, context):
        transform_func = lambda x: (x.get("id"), "{0} - {1}".format(x.get("name"), x.get("cidr")))
        return sorted([transform_func(x) for x in neutron_api.subnet_list(request)],
                      key=lambda x: x[0])

    def populate_protocol_choices(self, request, context):
        # TODO(mdurrant) - Return these from a service
        return [("","Select a protocol"),
                ("TCP", "TCP"),
                ("HTTP", "HTTP"),
                ("HTTPS", "HTTPS"),
                ("TERMINATED_HTTPS", "Terminated HTTPS")
        ]


    class Meta(object):
        name = _("LB Name and Subnet")
        # TODO(mdurrant) - Add a10-specific permissions
        permissions = ("openstack.services.network", )
        help_text = _("Specify the details for the VIP below")


class CreateVipAction(workflows.Action):
    listener_name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    listener_description = forms.CharField(label=_("Description"), min_length=1,
                                  max_length=255, required=False)
    protocol = forms.ChoiceField(label=_("Protocol"), required=True)
    protocol_port = forms.IntegerField(label=_("Protocol Port"), min_value=1, max_value=65535, required=True)

    def populate_vip_subnet_choices(self, request, context):
        return instance_utils.subnet_field_data(request, True)

    def populate_protocol_choices(self, request, context):
        # TODO(mdurrant) - Return these from a service
        return [("","Select a protocol"),
                ("TCP", "TCP"),
                ("HTTP", "HTTP"),
                ("HTTPS", "HTTPS"),
                ("TERMINATED_HTTPS", "Terminated HTTPS")
        ]


    class Meta(object):
        name = _("Protocol Data")
        # TODO(mdurrant) - Add a10-specific permissions
        permissions = ("openstack.services.network", )
        help_text = _("Specify the details for the name and subnet of the VIP below")


class CreateLbStep(workflows.Step):
    action_class = CreateLbAction
    contributes = ("lb_name", "lb_description", "vip_subnet")


class CreateVipStep(workflows.Step):
    action_class = CreateVipAction
    contributes = ("listener_name", "listener_desc", "protocol", "protocol_port")


class CreateVipWorkflow(workflows.Workflow):
    slug = "addvip"
    name = _("Create VIP")
    default_steps = (CreateLbStep, CreateVipStep, )
    success_url = "horizon:project:a10vips:index"
    finalize_button_name = "Create VIP"

    def handle(self, request, context):
        # First, try to create the LB.  Make sure we get an IP back because we need it for the listener.
        # Then, try to create the listener.
        # If we fail, delete the LB.
        success = False
        lb = None

        try:
            lb_body = self._get_lb_body_from_context(context)
            lb = lbaasv2.create_loadbalancer(request, lb_body).get("loadbalancer")
            import pdb; pdb.set_trace()
            lb_id = lb.get("id")


            listener_body = self._get_listener_body_from_context(context)
            listener = lbaasv2.create_listener(request, listener_body)
            success = True
        except Exception as ex:
            # If we bomb here, delete the LB that was created.
            LOG.exception(ex)
            exceptions.handle(request, _("Could not create listener"))

        if not success and lb:
            lbaasv2.delete_loadbalancer(lb)

        return success

    def _get_lb_body_from_context(self, context):
        return { "loadbalancer": {
               "name": context.get("lb_name"),
               "description": context.get("lb_description"),
               "vip_subnet_id": context.get("vip_subnet")
        }}

    def _get_listener_body_from_context(self, context, lb_id):
        return {"listener": {
                "name": context.get("listener_name"),
                "description": context.get("listener_desc"),
                "loadbalancer_id": lb_id,
                "protocol": context.get("protocol"),
                "protocol_port": context.get("protocol_port")
        }}
