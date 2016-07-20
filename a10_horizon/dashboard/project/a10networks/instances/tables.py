# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.
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


LOG = logging.getLogger(__name__)


#TODO(orchestration) - Move this method to a shareable location.
def instance_manager_for(request):
    return im.InstanceManager(
        base.project_id_for(request),
        session=base.session_for(request))


class AddDeviceInstanceAction(tables.LinkAction):
    name = "adddeviceinstance"
    verbose_name = _("Add Device Instance")
    url = "horizon:project:a10instances:adddeviceinstance"
    icon = "plus"
    classes = ("ajax-modal",)


class DeleteDeviceInstanceAction(tables.Action):
    name = "deletedeviceinstance"
    verbose_name = _("Delete Device Instance")

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete A10 vThunder Device Instance",
            u"Delete A10 vThunder Device Instances",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of A10 vThunder Device Instance",
            u"Scheduled deletion of A10 vThunder Device Instances",
            count
        )

    def handle(self, data_table, request, object_ids):
        for obj_id in object_ids:
            instance_id = data_table.get_object_by_id(obj_id)["nova_instance_id"]
            a10api.delete_a10_appliance(request, obj_id)
            imgr = instance_manager_for(request)
            imgr.delete_instance(instance_id)
            # super(DeleteApplianceAction, self).handle(data_table, request, object_ids)


def get_instance_detail(datum):
    return reverse_lazy('horizon:project:instances:detail', args=[datum["nova_instance_id"]])


# class A10ApplianceTable(tables.DataTable):
#     id = tables.Column("id", verbose_name=_("ID"), hidden=True)
#     name = tables.Column("name", verbose_name=_("Hostname"), hidden=False, link=get_instance_detail)
#     ip = tables.Column("host", verbose_name="Management IP")
#     api_ver = tables.Column("api_version", verbose_name="API Version")
#     nova_instance_id = tables.Column("nova_instance_id", hidden=False, link=get_instance_detail)

#     class Meta(object):
#         name = "a10appliancestable"
#         verbose_name = _("A10 Appliances")
#         table_actions = ()
#         row_actions = ()


def get_instance_detail(datum):
    return reverse_lazy('horizon:project:instances:detail', args=[datum["nova_instance_id"]])


class A10DeviceInstanceTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    tenant_id = tables.Column("tenant_id", verbose_name=_("Tenant ID"), hidden=True)
    ip_address = tables.Column("ip_address", verbose_name=_("IP Address"), hidden=True)
    nova_instance_id = tables.Column("nova_instance_id", verbose_name=_("Nova Instance ID"),
                                     hidden=False, link=get_instance_detail)

    class Meta(object):
        name = "a10deviceinstancetable"
        verbose_name = "a10deviceinstancetable"
        table_actions = (AddDeviceInstanceAction, DeleteDeviceInstanceAction,)
        row_actions = (DeleteDeviceInstanceAction,)
