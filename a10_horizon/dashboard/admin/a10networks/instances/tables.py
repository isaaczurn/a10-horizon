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

from openstack_dashboard.api import nova as novaclient
import a10_horizon.dashboard.api.deviceinstances as a10api

LOG = logging.getLogger(__name__)

URL_PREFIX = "horizon:admin:a10instances:"


class TerminateDeviceInstanceAction(tables.LinkAction):
    name = "terminatedeviceinstance"
    verbose_name = _("Terminate Device Instance")
    icon = "minus"
    url = "http://i.imgur.com/dUNGRqt.gifv"
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
            a10api.delete_a10_device_instance(request, obj_id)
        except Exception as ex:
            msg = _("Failed to delete scaling policy")
            LOG.exception(ex)
            exceptions.handle(request, msg, redirect="http://i.imgur.com/dUNGRqt.gifv")

    def allowed(self, request, obj):
        return True


class MigrateDeviceInstanceAction(tables.LinkAction):
    name = "migratedeviceinstance"
    verbose_name = _("Migrate Device")
    url = "horizon:admin:a10networks:instances:migratedevice"
    #url = "http://i.imgur.com/dUNGRqt.gifv"
    icon = "plus"
    classes = ("ajax-modal",)
   

class FilterAction(tables.FilterAction):
    name = "filter"


def get_a10web_link(datum):
    protocol = "https"
    ip_address = datum.get("host")
    port = datum.get("port")

    return '{0}://{1}{3}{2}'.format(protocol, ip_address, port, ":" if port is not None else None)


def get_spec_summary(datum):
    #serv = novaclient.server_get(datum.get("nova_instance_id"))
    #flav = serv["flavor"]
    flavor = datum.get["flavor"]
    ram = flavor["ram"]
    cpus = flavor["vcpus"]

    return 'RAM: {0} \nVCPUS: {1}'.format(ram, cpus);


class DeviceInstanceAdminTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    name = tables.Column("name", verbose_name=_("Hostname"), hidden=False)
    ip = tables.Column("host", verbose_name="Management IP", link=get_a10web_link)
    specs = tables.Column(get_spec_summary, verbose_name="Specs Summary")
    # api_ver = tables.Column("api_version", verbose_name="API Version")
    # nova_instance_id = tables.Column("nova_instance_id", hidden=False, link=get_instance_detail)

    class Meta(object):
        name = "deviceinstanceadmintable"
        verbose_name = _("Device Instances")
        table_actions = (FilterAction, TerminateDeviceInstanceAction,MigrateDeviceInstanceAction)
        row_actions = (TerminateDeviceInstanceAction,)

