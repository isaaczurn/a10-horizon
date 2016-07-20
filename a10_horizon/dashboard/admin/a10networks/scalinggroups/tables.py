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


class DeleteScalingGroupAction(tables.DeleteAction, tables.BatchAction):
    name = "deletescalinggroup"
    verbose_name = _("Delete Scaling Group")

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Scaling Group",
            u"Delete Scaling Groups",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Scaling Group",
            u"Scheduled deletion of Scaling Groups",
            count
        )

    def handle(self, data_table, request, object_ids):
        for obj_id in object_ids:
            try:
                scaling_api.delete_a10_scaling_policy(request, obj_id)
                redirect = reverse(self.redirect_url)
            except Exception as ex:
                msg = _("Failed to delete scaling group")
                LOG.exception(ex)
                exceptions.handle(request, msg, redirect=self.redirect_url)

        return redirect(URL_PREFIX + "index")

    def allowed(self, request, obj):
        return True


def get_group_detail_link(datum):
    return reverse_lazy(URL_PREFIX + "scalinggroupdetail",
                        kwargs={"scaling_group_id": datum["id"]})


class ScalingGroupAdminTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), link=get_group_detail_link)
    # TODO(tenant name lookup)
    tenant_id = tables.Column("tenant_id", verbose_name=_("Tenant ID"), hidden=True)
    name = tables.Column("name", verbose_name="Name", link=get_group_detail_link)
    description = tables.Column("description", verbose_name="Description")

    class Meta(object):
        name = "scalinggroupadmintable"
        verbose_name = "scalinggroupadmintable"
        table_actions = (DeleteScalingGroupAction, )
        row_actions = (DeleteScalingGroupAction, )
