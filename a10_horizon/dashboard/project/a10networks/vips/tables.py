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
    LOG.warning("Could not import lbaasv2 dashboard API")



LOG = logging.getLogger(__name__)
URL_PREFIX = "horizon:project:a10vips:"



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

    def handle(self, data_table, request, object_ids):
        for obj_id in object_ids:
            try:
                lbaasv2_api.vip_delete(request, obj_id)
                redirect = reverse(self.redirect_url)
            except Exception as ex:
                msg = self.failure_message
                LOG.exception(ex)
                exceptions.handle(request, msg, redirect=self.redirect_url)

            self.success_url = self.redirect_url
            msg = _('VIP deleted.')
            messages.success(request, msg)

        return redirect(self.redirect_url)

    def allowed(self, request, obj):
        return True


class MigrateVipAction(tables.LinkAction):
    pass


class TestVipAction(tables.LinkAction):
    pass


class EditVipAction(tables.LinkAction):
    name = "editvip"
    verbose_name = _("Edit VIP")
    url = URL_PREFIX + "edit"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = ("network",)  # FIXME(mdurrant) - A10-specific policies?
    success_url = "horizon:project:a10scaling:index"

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

    class Meta(object):
        name = "viptable"
        verbose_name = "viptable"
        table_actions = (DeleteVipAction,)
        row_actions = (EditVipAction, DeleteVipAction, )
