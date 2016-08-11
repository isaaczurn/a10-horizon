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
import a10_horizon.dashboard.api.vips as a10api_vips


LOG = logging.getLogger(__name__)

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
            a10api_vips.delete_vip(request, obj_id)
        except Exception as ex:
            msg = _("Failed to delete scaling policy")
            LOG.exception(ex)
            exceptions.handle(request, msg, redirect="http://i.imgur.com/dUNGRqt.gifv")

    def allowed(self, request, obj):
        return True


class VipTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    ip_address = tables.Column("ip_address", verbose_name=_("IP Address"), hidden=True)
    #
    nova_instance_id = tables.Column("nova_instance_id", verbose_name=_("Nova Instance ID"),
                                     hidden=False, )

    class Meta(object):
        name = "viptable"
        verbose_name = "viptable"
        table_actions = ()
        row_actions = ()

    def get_viptable_data(self):
        return []
