# Copyright (C) 2016, A10 Networks Inc. All rights reserved.

import logging

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from horizon import exceptions
from horizon import messages
from horizon import tables

from constants import AGG_DICT
from constants import OP_DICT
from constants import UNIT_DICT

from a10_horizon.dashboard.api import scaling as scaling_api


LOG = logging.getLogger(__name__)
URL_PREFIX = "horizon:project:a10scaling:"

# This file has a lot of DRY violations sacrificing elegance for ease of maintenance


class AddScalingPolicyLink(tables.LinkAction):
    name = "addscalingpolicy"
    verbose_name = _("Add Scaling Policy")
    url = URL_PREFIX + "addscalingpolicy"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = ("network",)  # FIXME(mdurrant) - A10-specific policies?
    success_url = "horizon:project:a10scaling:index"


class UpdateScalingPolicyLink(tables.LinkAction):
    name = "a10scaling:updatescalingpolicy"
    verbose_name = _("Edit Scaling Policy")
    classes = ("btn-update", "ajax-modal")
    icon = "pencil"
    # url = URL_PREFIX + "updatescalingpolicy"
    # success_url = "horizon:project:a10scaling:index"

    def get_link_url(self, datum):
        base_url = reverse(URL_PREFIX + "updatescalingpolicy",
                           kwargs={'scaling_policy_id': datum["id"]})
        return base_url


class DeleteScalingPolicyAction(tables.DeleteAction):
    name = "deletescalingpolicy"
    verbose_name = _("Delete Scaling Policy")

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Scaling Policy",
            u"Delete Scaling Policies",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Scaling Policy",
            u"Scheduled deletion of Scaling Policies",
            count
        )

    def handle(self, data_table, request, object_ids):
        for obj_id in object_ids:
            try:
                scaling_api.delete_a10_scaling_policy(request, obj_id)
                redirect = reverse(self.redirect_url)
            except Exception as ex:
                msg = _("Failed to delete scaling policy")
                LOG.exception(ex)
                exceptions.handle(request, msg, redirect=self.redirect_url)

        return redirect(URL_PREFIX + "index")

    def allowed(self, request, obj):
        return True


class AddAlarmLink(tables.LinkAction):
    name = "addscalingalarm"
    verbose_name = _("Add Scaling Alarm")
    url = URL_PREFIX + "addalarm"
    classes = ("ajax-modal",)
    icon = "plus"
    alarm_rules = ("network",)  # FIXME(mdurrant) - A10-specific policies?
    success_url = "horizon:project:a10scaling:index"


class UpdateAlarmLink(tables.LinkAction):
    name = "a10scaling:updatescalingalarm"
    verbose_name = _("Edit Scaling Alarm")
    classes = ("btn-update", "ajax-modal")
    icon = "pencil"
    # url = URL_PREFIX + "updatescalingalarm"
    # success_url = "horizon:project:a10scaling:index"

    def get_link_url(self, datum):
        base_url = reverse(URL_PREFIX + "updatealarm",
                           kwargs={'id': datum["id"]})
        return base_url


class DeleteAlarmLink(tables.DeleteAction):
    name = "deletescalingalarm"
    verbose_name = _("Delete Scaling Alarm")
    redirect_url = reverse_lazy(URL_PREFIX + "index")
    failure_message = _('Failed to delete reaction')
    # method = "GET"

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Scaling Alarm",
            u"Delete Scaling Alarms",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Scaling Alarm",
            u"Scheduled deletion of Scaling Alarms",
            count
        )

    def handle(self, data_table, request, object_ids):
        for obj_id in object_ids:
            try:
                scaling_api.delete_a10_scaling_alarm(request, obj_id)
                redirect = reverse(self.redirect_url)
            except Exception as ex:
                msg = self.failure_message
                LOG.exception(ex)
                exceptions.handle(request, msg, redirect=self.redirect_url)

            self.success_url = self.redirect_url
            msg = _('Scaling Action deleted.')
            LOG.debug(msg)
            messages.success(request, msg)

        return redirect(self.redirect_url)

    def allowed(self, request, obj):
        return True


class AddActionLink(tables.LinkAction):
    name = "addscalingaction"
    verbose_name = _("Add Scaling Action")
    url = URL_PREFIX + "addaction"
    classes = ("ajax-modal",)
    icon = "plus"
    action_rules = ("network",)  # FIXME(mdurrant) - A10-specific policies?
    success_url = "horizon:project:a10scaling:index"


class UpdateActionLink(tables.LinkAction):
    name = "updatescalingaction"
    verbose_name = _("Edit Scaling Action")
    classes = ("btn-update", "ajax-modal")
    icon = "pencil"

    def get_link_url(self, datum):
        base_url = reverse(URL_PREFIX + "updateaction",
                           kwargs={'id': datum["id"]})
        return base_url


class DeleteActionLink(tables.DeleteAction):
    name = "deletescalingaction"
    verbose_name = _("Delete Scaling Action")
    redirect_url = reverse_lazy(URL_PREFIX + "index")
    failure_message = _('Failed to delete reaction')

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Scaling Action",
            u"Delete Scaling Actions",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Scaling Action",
            u"Scheduled deletion of Scaling Actions",
            count
        )

    def handle(self, data_table, request, object_ids):
        for obj_id in object_ids:
            try:
                scaling_api.delete_a10_scaling_action(request, obj_id)
                redirect = reverse(self.redirect_url)
            except Exception as ex:
                msg = self.failure_message
                LOG.exception(ex)
                exceptions.handle(request, msg, redirect=self.redirect_url)

            self.success_url = self.redirect_url
            msg = _('Scaling Action deleted.')
            messages.success(request, msg)

        return redirect(self.redirect_url)

    def allowed(self, request, obj):
        return True


class AddReactionLink(tables.LinkAction):
    name = "addreaction"
    verbose_name = _("Add Scaling Reaction")
    classes = ("ajax-modal",)
    icon = "plus"
    url = URL_PREFIX + "addreaction"

    def get_link_url(self, datum=None):
        id = None
        if datum is not None and "id" in datum:
            id = datum["id"]
        else:
            id = self.table.kwargs["scaling_policy_id"]
        return reverse(self.url, kwargs={'scaling_policy_id': id})


class DeleteReactionLink(tables.DeleteAction):
    name = "deletereaction"
    verbose_name = _("Delete Reaction")
    icon = "minus"
    _redirect_url = URL_PREFIX + "scalingpolicydetail"
    failure_message = _('Failed to delete reaction')

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Reaction",
            u"Delete Reactions",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of scaling reaction",
            u"Scheduled deletion of scaling reactions",
            count
        )

    def _remove_deleted(self, reactions, object_ids):
        rv = reactions
        if len(reactions) > 0:
                position = 0
                for reaction in reactions:
                    reaction["position"] = int(position)
                    position += 1

                for obj_id in object_ids:
                    reaction = None
                    try:
                        reaction = reactions[int(obj_id)]
                    except Exception as ex:
                        LOG.exception(ex)

                    if reaction:
                        del reactions[int(obj_id)]

        return rv

    def handle(self, data_table, request, obj_ids):
        scaling_policy_id = data_table.kwargs.get("scaling_policy_id", None)
        self.redirect_url = reverse(self._redirect_url,
                                    kwargs={"scaling_policy_id": scaling_policy_id})
        self.success_url = self.redirect_url
        reaction = None

        try:
            existing_policy = scaling_api.get_a10_scaling_policy(request, scaling_policy_id)
            reactions = self._remove_deleted(existing_policy.reactions, obj_ids)

            if len(reactions) > 0:
                position = 0
                for reaction in reactions:
                    reaction["position"] = int(position)
                    position += 1

                reaction = None
                for obj_id in obj_ids:
                    try:
                        reaction = reactions[int(obj_id)]
                    except Exception as ex:
                        pass
                    if reaction:
                        del reactions[int(obj_id)]

        except Exception as ex:
            msg = self.failure_message
            LOG.exception(ex)
            # redirect = self.redirect_url
            exceptions.handle(request, msg, redirect=redirect)

        existing_policy = existing_policy.to_dict()
        existing_policy["reactions"] = map(lambda x:
                                           {
                                               "alarm_id": x["alarm_id"],
                                               "action_id": x["action_id"]
                                           },
                                           reactions)
        del existing_policy["tenant_id"]

        try:
            scaling_api.update_a10_scaling_policy(request, **existing_policy)
            self.success_url = self.redirect_url
            # redirect = self.success_url
            msg = _('Reaction deleted.')
            LOG.debug(msg)
            messages.success(request, msg)

        except Exception as ex:
            msg = self.failure_message
            LOG.exception(ex)
            # redirect = self.redirect_url
            exceptions.handle(request, msg, redirect=self.redirect_url)

        return redirect(str(self.success_url))

    def allowed(self, request, obj):
        return True


def get_group_detail_link(datum):
    return reverse_lazy(URL_PREFIX + "scalinggroupdetail", kwargs={"scaling_group_id": datum["id"]})


class A10ScalingGroupTable(tables.DataTable):
    # form fields
    id = tables.Column("id", verbose_name=_("ID"), link=get_group_detail_link)
    # TODO(tenant name lookup?)
    tenant_id = tables.Column("tenant_id", verbose_name=_("Tenant ID"), hidden=True)
    name = tables.Column("name", verbose_name="Name", link=get_group_detail_link)
    description = tables.Column("description", verbose_name="Description")

    class Meta(object):
        name = "a10scalinggrouptable"
        verbose_name = _("Scaling Groups")
        table_actions = ()
        row_actions = ()


class A10ScalingGroupMemberTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    scaling_group_id = tables.Column("scaling_group_id", verbose_name=_("Scaling Group ID"),
                                     hidden=True)
    tenant_id = tables.Column("tenant_id", verbose_name=_("Tenant ID"), hidden=True)
    name = tables.Column("name", verbose_name=("Name"))
    host = tables.Column("host", verbose_name=_("Host"))
    nova_instance_id = tables.Column("nova_instance_id", verbose_name="Instance ID")

    class Meta(object):
        name = "a10scalinggroupmembertable"
        verbose_name = _("Scaling Group Members")
        table_actions = ()
        row_actions = ()


def get_policy_detail(datum):
    return reverse_lazy(URL_PREFIX + "scalingpolicydetail",
                        kwargs={"scaling_policy_id": datum["id"]})


class A10ScalingPolicyTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    name = tables.Column("name", verbose_name=("Name"), link=get_policy_detail)
    description = tables.Column("description", verbose_name=_("Description"))
    cooldown = tables.Column("cooldown", verbose_name=_("Cooldown Period"))
    min_instances = tables.Column("min_instances", verbose_name=_("Min. Instances"))
    max_instances = tables.Column("max_instances", verbose_name=_("Max. Instances"))

    class Meta(object):
        name = "a10scalingpolicytable"
        verbose_name = _("Scaling Policies")
        table_actions = (AddScalingPolicyLink, DeleteScalingPolicyAction)
        row_actions = (UpdateScalingPolicyLink, DeleteScalingPolicyAction)


def reaction_summary(alarm, action):
    """Pretty print a reaction in the following format:

    When {agg} {measurement} is {operator} {threshold}...
        {unit} over a period of {period} {period_unit}.
        {action} {amount} instances.
    """

    # TODO(mdurrant) - Insert brains for singular/plurals.
    # If period > 1 period_units
    # If |threshold| > 1 units
    alarm_fmt = "When {0} {1} is {2} {3} {4} over a period of {5} {6}"
    action_fmt = "{0} by {1} instances."
    alarm_txt = alarm_fmt.format(AGG_DICT.get(alarm["aggregation"]),
                                 alarm["measurement"], OP_DICT.get(alarm["operator"]),
                                 alarm["threshold"], UNIT_DICT.get(alarm["unit"]),
                                 alarm["period"], alarm["period_unit"])
    action_txt = action_fmt.format(action["action"], action["amount"])

    return "{0}, {1}".format(alarm_txt, action_txt)


class UpdatePolicyReactionTable(tables.DataTable):
    position = tables.Column("position", verbose_name=_("Position"), hidden=True)
    alarm_id = tables.Column("alarm_id", hidden=True)
    action_id = tables.Column("action_id", hidden=True)
    alarm_name = tables.Column(lambda x: x["alarm"]["name"],
                               verbose_name=_("Alarm"),
                               link=(lambda x: reverse_lazy(URL_PREFIX + "updatealarm",
                                                            kwargs={"id": x["alarm_id"]})))
    action_name = tables.Column(lambda x: x["action"]["name"],
                                verbose_name=_("Action"),
                                link=(lambda x: reverse_lazy(URL_PREFIX + "updateaction",
                                                             kwargs={"id": x["action_id"]})))

    summary = tables.Column(lambda x: reaction_summary(x["alarm"], x["action"]),
                            verbose_name=_("Summary"))

    def get_object_id(self, datum):
        return datum['position']

    class Meta(object):
        name = "updatepolicyreactiontable"
        verbose_name = _("Scaling Policy Reactions")
        table_actions = (AddReactionLink,)
        row_actions = (DeleteReactionLink, )


class A10ScalingAlarmTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    tenant_id = tables.Column("tenant_id", verbose_name=_("Tenant ID"), hidden=True)
    name = tables.Column("name", verbose_name="Name")
    description = tables.Column("description", verbose_name="Description")
    aggregation = tables.Column("aggregation", verbose_name="Aggregation")
    measurement = tables.Column("measurement", verbose_name="Measurement")
    operator = tables.Column("operator", verbose_name="Operator")
    threshold = tables.Column("threshold", verbose_name="Threshold")
    unit = tables.Column("unit", verbose_name="Unit")
    period = tables.Column("period", verbose_name="Period")
    period_unit = tables.Column("period_unit", verbose_name="period_unit")

    class Meta(object):
        name = "a10scalingalarmtable"
        verbose_name = _("Scaling Alarms")
        table_actions = (AddAlarmLink, DeleteAlarmLink)
        row_actions = (UpdateAlarmLink, DeleteAlarmLink)


class A10ScalingActionTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    tenant_id = tables.Column("tenant_id", verbose_name=_("Tenant ID"), hidden=True)
    name = tables.Column("name", verbose_name="Name")
    description = tables.Column("description", verbose_name="Description")
    action = tables.Column("action", verbose_name="Action")
    amount = tables.Column("amount", verbose_name="Amount")

    class Meta(object):
        name = "a10scalingactiontable"
        verbose_name = _("Scaling Actions")
        table_actions = (AddActionLink, DeleteActionLink)
        row_actions = (UpdateActionLink, DeleteActionLink)
