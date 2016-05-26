# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.

import logging

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

# from openstack_dashboard import api
from a10_horizon.dashboard.api import scaling as api
from a10_neutronclient.resources import a10_scaling_group as scaling_resources


LOG = logging.getLogger(__name__)


def array_to_choices(choices=[]):
    return map(lambda x: (x, x), choices)


class UpdatePolicy(forms.SelfHandlingForm):
    def __init__(self, *args, **kwargs):
        super(UpdatePolicy, self).__init__(*args, **kwargs)
        self.submit_url = kwargs.get("id")

    id = forms.CharField(label=_("ID"), widget=forms.TextInput(attrs={'readonly': 'readonly'}))
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

    failure_url = "horizon:project:a10scaling:index"
    success_url = "horizon:project:a10scaling:index"
    # redirect_url = reverse_lazy('horizon:project:a10scaling:updatescalingpolicy')

    def handle(self, request, context):
        try:
            policy = api.update_a10_scaling_policy(request, **context)
            msg = _("Scaling Policy {0} was successfully updated").format(context["name"])
            messages.success(request, msg)
            return policy
        except Exception as ex:
            msg = _("Failed to update Scaling Policy %s") % context["name"]
            LOG.exception(ex)
            redirect = reverse_lazy(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)


class UpdateAlarm(forms.SelfHandlingForm):
    id = forms.CharField(label=_("ID"), widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    description = forms.CharField(label=_("Description"), min_length=1,
                                  max_length=255, required=False)
    aggregation = forms.ChoiceField(label=_("Aggregation"),
                                    choices=array_to_choices(scaling_resources.ALARM_AGGREGATIONS),
                                    required=True)
    measurement = forms.ChoiceField(label=_("Measurement"),
                                    choices=array_to_choices(scaling_resources.ALARM_MEASUREMENTS),
                                    required=True)
    operator = forms.ChoiceField(label=_("Operator"),
                                 choices=array_to_choices(scaling_resources.ALARM_OPERATORS),
                                 required=True,)
    threshold = forms.FloatField(label=_("Threshold"),
                                 required=True)
    unit = forms.DynamicChoiceField(label=_("Unit"),
                                    choices=array_to_choices(scaling_resources.ALARM_UNITS),
                                    required=True)
    period = forms.IntegerField(label=_("Period"),
                                required=True)
    period_unit = forms.ChoiceField(label=_("Period Unit"),
                                    choices=array_to_choices(scaling_resources.ALARM_PERIOD_UNITS),
                                    required=True)

    failure_url = "horizon:project:a10scaling:index"
    success_url = "horizon:project:a10scaling:index"

    def handle(self, request, context):
        try:
            alarm = api.update_a10_scaling_alarm(request, **context)
            msg = _("Scaling Alarm {0} was successfully updated").format(context["name"])
            messages.success(request, msg)
            return alarm
        except Exception as ex:
            msg = _("Failed to update Scaling Action")
            LOG.exception(ex)
            redirect = reverse_lazy(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)


class UpdateAction(forms.SelfHandlingForm):
    id = forms.CharField(label=_("ID"), widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    description = forms.CharField(label=_("Description"), min_length=1,
                                  max_length=255, required=False)
    action = forms.ChoiceField(label=_("Action"),
                               choices=array_to_choices(scaling_resources.ACTIONS),
                               required=True)
    amount = forms.IntegerField(label=_("Amount"), required=True)

    failure_url = "horizon:project:a10scaling:index"
    success_url = "horizon:project:a10scaling:index"

    def handle(self, request, context):
        try:
            action = api.update_a10_scaling_action(request, **context)
            msg = _("Scaling Action was successfully updated")
            messages.success(request, msg)
            return action
        except Exception as ex:
            msg = _("Failed to update Scaling Action")
            LOG.exception(ex)
            redirect = reverse_lazy(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
