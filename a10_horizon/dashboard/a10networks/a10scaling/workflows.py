# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.

import logging

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import workflows

# a10_horizon.dashboard.api.client.Client extends neutron.api.client.Client
from a10_neutronclient.resources import a10_scaling_group as scaling_resources
from a10_horizon.dashboard.api import scaling as api


LOG = logging.getLogger(__name__)


class AddPolicyAction(workflows.Action):
    name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    description = forms.CharField(label=_("Description"), min_length=1,
                                  max_length=255, required=False)
    # TODO(mdurrant) - Get min/max cooldown/instances from config?
    cooldown = forms.IntegerField(label=_("Cooldown Period in Seconds"),
                                  min_value=1,
                                  max_value=65536,
                                  required=True)
    min_instances = forms.IntegerField(label=_("Minimum Instances"),
                                       min_value=1,
                                       required=True)
    max_instances = forms.IntegerField(label=_("Maximum Instances"),
                                       required=False)

    class Meta(object):
        name = _("Create New Scaling Policy")
        # TODO(mdurrant) - Add a10-specific permissions
        permissions = ("openstack.services.network", )
        help_text = _("Specify the details for the scaling policy below")


class AddPolicyStep(workflows.Step):
    action_class = AddPolicyAction
    contributes = ("name", "description", "cooldown", "min_instances", "max_instances")


class AddPolicyWorkflow(workflows.Workflow):
    slug = "addscalingpolicy"
    name = _("Add Scaling Policy")
    default_steps = (AddPolicyStep, )
    success_url = "horizon:project:a10scaling:index"
    finalize_button_name = "Create Scaling Policy"

    def handle(self, request, context):
        success = True
        try:
            api.create_a10_scaling_policy(request, **context)
        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to create scaling policy"))
        return success


class DeletePolicyWorkflow(workflows.Workflow):
    name = "deletescalingpolicy"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of %(data_type)s")
    data_type_singular = _("Scaling Policy")
    data_type_plural = _("Scaling Policies")

    def handle(self, data_table, request, object_ids):
        for obj_id in object_ids:
            try:
                api.delete_a10_scaling_policy(request, obj_id)
                redirect_url = 'horizon:project:a10scaling:index'
            except Exception as ex:
                LOG.exception(ex)
                exceptions.handle(request, _("Unable to delete scaling policy"))

        return redirect(redirect_url)


class AddActionAction(workflows.Action):
    name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    description = forms.CharField(label=_("Description"), min_length=1,
                                  max_length=255, required=False)
    action = forms.ChoiceField(label=_("Action"),
                               choices=map(lambda x: (x, x), scaling_resources.ACTIONS),
                               required=True)
    amount = forms.IntegerField(label=_("Amount"), required=True)

    class Meta(object):
        name = _("Create New Scaling Action")
        # TODO(mdurrant) - Add a10-specific permissions
        permissions = ("openstack.services.network", )
        help_text = _("Specify the details for the scaling action below")


class AddActionStep(workflows.Step):
    action_class = AddActionAction
    contributes = ("name", "description", "action", "amount",)


class AddActionWorkflow(workflows.Workflow):
    slug = "addscalingaction"
    name = _("Add Scaling Action")
    default_steps = (AddActionStep, )
    success_url = "horizon:project:a10scaling:index"
    finalize_button_name = "Create Action"

    def handle(self, request, context):
        try:
            api.create_a10_scaling_action(request, **context)
        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to delete scaling action"))
        return redirect(self.success_url)


class DeleteScalingActionAction(tables.BatchAction):
    name = "deletescalingaction"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of %(data_type)s")
    data_type_singular = _("Scaling Action")
    data_type_plural = _("Scaling Policies")
    success_url = "horizon:project:a10scaling:index"

    def handle(self, data_table, request, object_ids):
        for obj_id in object_ids:
            try:
                api.delete_a10_scaling_action(request, obj_id)
            except Exception as ex:
                LOG.exception(ex)
                exceptions.handle(request, _("Unable to delete scaling alarms"))

        return redirect(self.success_url)


class AddAlarmAction(workflows.Action):
    name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    description = forms.CharField(label=_("Description"), min_length=1,
                                  max_length=255, required=False)
    aggregation = forms.DynamicChoiceField(label=_("Aggregation"),
                                           choices=map(lambda x: (x, x),
                                                       scaling_resources.ALARM_AGGREGATIONS),
                                           required=True)
    measurement = forms.ChoiceField(label=_("Measurement"),
                                    choices=map(lambda x: (x, x),
                                                scaling_resources.ALARM_MEASUREMENTS),
                                    required=True)
    operator = forms.ChoiceField(label=_("Operator"),
                                 choices=map(lambda x: (x, x),
                                             scaling_resources.ALARM_OPERATORS),
                                 required=True,)
    threshold = forms.FloatField(label=_("Threshold"),
                                 required=True)
    unit = forms.DynamicChoiceField(label=_("Unit"),
                                    choices=map(lambda x: (x, x),
                                                scaling_resources.ALARM_UNITS),
                                    required=True)
    period = forms.IntegerField(label=_("Period"),
                                required=True)
    period_unit = forms.ChoiceField(label=_("Period Unit"),
                                    choices=map(lambda x: (x, x),
                                                scaling_resources.ALARM_PERIOD_UNITS),
                                    required=True)

    class Meta(object):
        name = _("Create New Scaling Alarm")
        # TODO(mdurrant) - Add a10-specific permissions
        permissions = ("openstack.services.network", )
        help_text = _("Specify the details for the scaling action below")


class AddAlarmStep(workflows.Step):
    action_class = AddAlarmAction
    contributes = ("name", "description", "aggregation", "measurement", "operator",
                   "threshold", "unit", "period", "period_unit")


class AddScalingAlarmWorkflow(workflows.Workflow):
    slug = "addscalingalarm"
    name = _("Add Scaling Alarm")
    default_steps = (AddAlarmStep, )
    success_url = "horizon:project:a10scaling:index"
    finalize_button_name = "Create Alarm"

    def handle(self, request, context):
        success = True
        try:
            api.create_a10_scaling_alarm(request, **context)
        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to create scaling alarms"))
        return success


class DeleteScalingAlarmAction(tables.BatchAction):
    name = "deletescalingalarm"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of %(data_type)s")
    data_type_singular = _("Scaling Alarm")
    data_type_plural = _("Scaling Policies")

    def handle(self, data_table, request, object_ids):
        for obj_id in object_ids:
            try:
                api.delete_a10_scaling_alarm(request, obj_id)
            except Exception as ex:
                LOG.exception(ex)
                exceptions.handle(request, _("Unable to delete scaling alarms"))

        return redirect("horizon:project:a10scaling:index")


class AddReactionAction(workflows.Action):
    scaling_policy_id = forms.Field(widget=forms.HiddenInput, initial="")
    alarm_id = forms.ChoiceField(label=_("Alarm"))
    action_id = forms.ChoiceField(label=_("Action"))
    detail_url = "horizon:project:a10scaling:scalingpolicydetail"

    def __init__(self, request, *args, **kwargs):
        alarms = []
        actions = []
        # Make it so we don't have to pull this out of the tuples arg.
        policy_id = args[0]["scaling_policy_id"]

        alarm_choices = [('', _('Select an alarm'))]
        action_choices = [('', _('Select an action'))]
        super(AddReactionAction, self).__init__(request, *args, **kwargs)

        try:
            alarms = api.get_a10_scaling_alarms(request)
        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to retrieve scaling alarms"))

        try:
            actions = api.get_a10_scaling_actions(request)
        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to retrieve scaling alarms"))

        choice_map = lambda x: (x["id"], x["name"])

        map(alarm_choices.append, map(choice_map, alarms))
        map(action_choices.append, map(choice_map, actions))

        self.fields["scaling_policy_id"].value = policy_id
        self.fields["alarm_id"].choices = alarm_choices
        self.fields["action_id"].choices = action_choices
        self.success_url = reverse_lazy(self.detail_url,
                                        kwargs={"scaling_policy_id": policy_id})

    def _convert_reactions(self, reactions):
        """Extracts action/alarm IDs from reactions retrieved via Neutron API"""
        return map(lambda x: {"alarm_id": x["alarm_id"],
                              "action_id": x["action_id"]}, reactions)

    def handle(self, request, context):
        policy_id = context["scaling_policy_id"]

        try:
            policy = api.get_a10_scaling_policy(request, policy_id)
            reactions = self._convert_reactions(policy.reactions)
        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to retrieve existing policy."))
            return False

        try:
            # Extract the IDs from the reactions since that's all we need
            map(reactions.append, self._convert_reactions([context]))

            # convert to dictioary for API
            policy = policy.to_dict()
            policy["reactions"] = reactions

            # read only attribute, this should probably go in clean()
            del policy["tenant_id"]

            api.update_a10_scaling_policy(request, **policy)

        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to update policy."))
            return False

        return True

    class Meta(object):
        name = _("Add Scaling Reaction")
        permissions = ('openstack.services.network',)
        help_text = _("Specify reactions for the scaling policy")


class AddReactionStep(workflows.Step):
    action_class = AddReactionAction
    contributes = ("scaling_policy_id", "alarm_id", "action_id")


class AddReactionWorkflow(workflows.Workflow):
    slug = "addreaction"
    name = _("Add Scaling Reaction")
    default_steps = (AddReactionStep, )
    finalize_button_name = "Create Reaction"
    redirect_url = "horizon:project:a10scaling:index"
    detail_url = "horizon:project:a10scaling:scalingpolicydetail"
    success_message = _("Created Scaling Reaction")  # noqa
    failure_message = _("Unable to create scaling reaction")  # noqa

    def handle(self, request, context):
        success = True
        # Get the existing policy
        try:
            scaling_policy_id = context["scaling_policy_id"]
            self.success_url = reverse_lazy(self.detail_url,
                                            kwargs={"scaling_policy_id": scaling_policy_id})
            policy = api.get_a10_scaling_policy(request, scaling_policy_id)
            context["scaling_policy"] = policy
            success = True
        except Exception as ex:
            LOG.exception(ex)
            exceptions.handle(request, _("Unable to add scaling reaction"))
        # Re-assign order as needed.

        return success
