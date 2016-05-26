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
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables

import a10_horizon.dashboard.api.a10devices as a10api
import a10_horizon.dashboard.api.base as base
import a10_neutron_lbaas.vthunder.instance_manager as im

LOG = logging.getLogger(__name__)


#TODO(orchestration) - Move this method to a shareable location.
def instance_manager_for(request):
    return im.InstanceManager(
        base.project_id_for(request),
        session=base.session_for(request))


class AddApplianceAction(tables.LinkAction):
    name = "addappliance"
    verbose_name = _("Create Appliance")
    url = "horizon:project:a10appliances:addappliance"
    icon = "plus"
    classes = ("ajax-modal",)


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


class A10ApplianceTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    name = tables.Column("name", verbose_name=_("Hostname"), hidden=False)
    ip = tables.Column("host", verbose_name="Management IP")
    api_ver = tables.Column("api_version", verbose_name="API Version")
    nova_instance_id = tables.Column("nova_instance_id", hidden=True)
    class Meta(object):
        name = "a10appliancestable"
        verbose_name = _("A10 Appliances")
        table_actions = ()
        row_actions = ()


class A10DeviceInstanceTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    tenant_id = tables.Column("tenant_id", verbose_name=_("Tenant ID"), hidden=True)
    ip_address = tables.Column("ip_address", verbose_name=_("IP Address"), hidden=True)
    nova_instance_id = tables.Column("nova_instance_id", verbose_name=_("Nova Instance ID"),
                                     hidden=True)

    class Meta(object):
        name = "a10deviceinstancetable"
        verbose_name = "a10deviceinstancetable"
        table_actions = ()
        row_actions = ()
