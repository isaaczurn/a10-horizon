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


LOG = logging.getLogger(__name__)


class MigrateDeviceInstanceAction(tables.LinkAction):
    name = "migratedeviceinstance"
    verbose_name = _("Migrate...")
    url = "horizon:project:a10appliances:addappliance"
    icon = "plus"
    classes = ("ajax-modal",)


class TerminateDeviceInstanceAction(tables.Action):
    name = "terminatedeviceinstance"
    verbose_name = _("Terminate Device Instance")
    url = "horizon:admin:a10networks:instances:deleteinstance"
    icon = "minus"
    classes = ("ajax-modal", )

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Terminate Device Instance",
            u"Terminate Device Instance",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of A10 Device Instance",
            u"Scheduled deletion of A10 Device Instance",
            count
        )

    def handle(self, data_table, request, object_ids):
        for obj_id in object_ids:
            instance_id = data_table.get_object_by_id(obj_id)["nova_instance_id"]
            a10api.delete_a10_appliance(request, obj_id)
            imgr = instance_manager_for(request)
            imgr.delete_instance(instance_id)
            # super(DeleteApplianceAction, self).handle(data_table, request, object_ids)


class DeviceInstanceAdminTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    name = tables.Column("name", verbose_name=_("Hostname"), hidden=False)
    ip = tables.Column("host", verbose_name="Management IP")
    # api_ver = tables.Column("api_version", verbose_name="API Version")
    # nova_instance_id = tables.Column("nova_instance_id", hidden=False, link=get_instance_detail)

    class Meta(object):
        name = "deviceinstanceadmintable"
        verbose_name = _("Device Instances")
        table_actions = (TerminateDeviceInstanceAction,)
        row_actions = (TerminateDeviceInstanceAction,)
