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

# from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables

import a10_horizon.dashboard.api.deviceinstances as a10api

import workflows as a_workflows

LOG = logging.getLogger(__name__)

URL_PREFIX = "horizon:admin:a10instances:"


class TerminateDeviceInstanceAction(tables.DeleteAction):
    name = "terminatedeviceinstance"
    verbose_name = _("TTerminate Device Instance")
    icon = "minus"
    # classes = ("ajax-modal", )
    # policy_rules = ()

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Terminate Device Instance",
            u"Terminate Device Instances",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of A10 Device Instance",
            u"Scheduled deletion of A10 Device Instances",
            count
        )

    def handle(self, request, obj_ids):
        pass

    def delete(self, request, obj_id):
        try:
            a10api.delete_a10_appliance(request, obj_id)
        except Exception as ex:
            msg = _("Failed to delete scaling policy")
            LOG.exception(ex)
            exceptions.handle(request, msg, redirect="http://google.com")

    def allowed(self, request, obj):
        return True

class MigrateDeviceInstanceAction(tables.LinkAction):
    name = "migratedevice"
    verbose_name = _("Migrate Device")
    icon = "plus"
    url = "horizon:admin:a10deviceinstances:migratedevice"
    action_type = "danger"

    classes = ("ajax-modal",)

def get_instance_detail(datum):
    return reverse_lazy('horizon:project:instances:detail', args=[datum["nova_instance_id"]])

def get_a10web_link(datum):
    protocol = "https"
    ip_address = datum.get("host")
    port = datum.get("port")

    return 'https://{0}'.format(ip_address)

def get_compute_link(datum):
    hyper_id = "{0}_{1}".format(datum["comp_id"], datum["comp_name"])
    return reverse_lazy('horizon:admin:hypervisors:detail', kwargs={"hypervisor": hyper_id})

def get_spec_summary(datum):
    flavor = datum.get("flavor")
    if flavor:
        ram = flavor.ram
        cpus = flavor.vcpus
        return 'RAM: {0}   VCPUS: {1}'.format(ram, cpus)

class DeviceInstanceAdminTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    name = tables.Column("name", verbose_name=_("Hostname"), hidden=False)
    owner = tables.Column("owner", verbose_name=_("Owner"), hidden=False)
    image = tables.Column("image", verbose_name=_("Image"), hidden=False)
    ip_address = tables.Column("host", link=get_a10web_link, verbose_name=_("IP Address"), hidden=False,)
    specs = tables.Column(get_spec_summary, verbose_name="Specs Summary")
    comp_name = tables.Column("comp_name", link=get_compute_link, verbose_name=_("Compute Node"), hidden=False,)
    nova_instance_id = tables.Column("nova_instance_id", verbose_name=_("Nova Instance ID"),
                                     hidden=False, link=get_instance_detail)

    class Meta(object):
        name = "deviceinstanceadmintable"
        verbose_name = _("Device Instances")
        table_actions = (MigrateDeviceInstanceAction, TerminateDeviceInstanceAction,)
        row_actions = (MigrateDeviceInstanceAction, TerminateDeviceInstanceAction,)
