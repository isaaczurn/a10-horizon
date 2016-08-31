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

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables

# lbaasv2 api
try:
    from neutron_lbaas_dashboard.api import lbaasv2 as lbaasv2_api
except ImportError as ex:
    LOG.exception(ex)
    LOG.error("Could not import lbaasv2 dashboard API")


LOG = logging.getLogger(__name__)
URL_PREFIX = "horizon:project:a10vips:"


class CreateVipLink(tables.LinkAction):
    name = "createvip"
    verbose_name = _("Create VIP")
    url = URL_PREFIX + "create"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = ("network",)  # FIXME(mdurrant) - A10-specific policies?
    success_url = "horizon:project:a10vips:index"


class DeleteVipAction(tables.DeleteAction):
    name = "deletevip"
    verbose_name = _("Delete VIP")
    redirect_url = reverse_lazy(URL_PREFIX + "index")
    failure_message = _('Failed to delete VIP')

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete VIP",
            u"Delete VIPs",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of VIP",
            u"Scheduled deletion of VIPs",
            count
        )

    def allowed(self, request, obj):
        return True


class MigrateVipAction(tables.LinkAction):
    pass


class TestVipAction(tables.Action):
    name = "testvip"
    verbose_name = _("Test VIP")
    url = URL_PREFIX + "test"
    classes = tuple()
    policy_rules = ("network",)
    success_url = "horizon:project:a10vips:index"
    method = "GET"
    requires_input = True
    enabled = False

    def single(self, data_table, request, object_id):
        # Test methods need to be put into a lib
        # Start low level - ping, tcp, http, https
        return True

    def allowed(self, request, obj):
        # Put in logic here for whether or not we can actually test something.
        # This will allow is to do simple TCP tests in the beginning and slowly expand our wheelhouse.
        return True


class EditVipAction(tables.LinkAction):
    name = "editvip"
    verbose_name = _("Edit VIP")
    url = URL_PREFIX + "edit"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = ("network",)  # FIXME(mdurrant) - A10-specific policies?
    success_url = "horizon:project:a10vips:index"

    def get_link_url(self, datum):
        base_url = reverse(URL_PREFIX + "edit",
                           kwargs={'id': datum["id"]})
        return base_url


class VipTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    ip_address = tables.Column("vip_address", verbose_name=_("IP Address"))
    provision_status = tables.Column("provisioning_status",
                                     verbose_name=_("Provisioning Status"))
    provider = tables.Column("provider", verbose_name=_("Provider"))
    op_status = tables.Column("op_status",
                              verbose_name=_("Operating Status"))
    name = tables.Column("name", verbose_name=_("Name"))
    owner = tables.Column("owner", verbose_name=_("Owner"))

    def get_object_id(self, datum):
        return datum.get("id")

    class Meta(object):
        name = "viptable"
        verbose_name = "viptable"
        table_actions = (CreateVipLink, DeleteVipAction,)
        row_actions = (EditVipAction,
                       DeleteVipAction,
                       TestVipAction)
