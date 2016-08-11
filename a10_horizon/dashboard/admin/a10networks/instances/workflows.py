# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.
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

from a10_horizon.dashboard.api import deviceinstances


from a10_horizon.dashboard.api import deviceinstances

import helper


def array_to_choices(choices):
    return map(lambda x: (x, x), choices)


class MigrateDeviceAction(workflows.Action):

    nova_instance_id = forms.CharField(label=_("Nova Instance ID"),
                                  widget=forms.HiddenInput(),
                                  required=True)
    host = forms.ChoiceField(label=_("Host IP"),
                             required=True)

    def __init__(self, request, *args, **kwargs):
        super(MigrateDeviceAction, self).__init__(request, *args, **kwargs)

    def populate_host_choices(self, request, context):
        host_list = helper.get_hosts(request)
        return array_to_choices(host_list)

    class Meta(object):
        name = _("Migrate Device")
        help_text = _("Migrate device to a new host")

class MigrateDeviceStep(workflows.Step):
    action_class = MigrateDeviceAction
    contributes = ("nova_instance_id", "host")

class MigrateDeviceWorkflow(workflows.Workflow):
    slug = "migratedevice"
    name = _("Migrate Device")
    default_steps = (MigrateDeviceStep, )
    success_url = "horizon:admin:a10deviceinstances"
    finalize_button_name = "Create Migration"

    def handle(self, request, context):
        success = True
        try:
            migrate = helper.migrate(request,
                                     context['nova_instance_id'],
                                     context['host'])
        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to migrate"))
        return success
