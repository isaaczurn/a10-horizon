# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
import logging

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from horizon import messages
from horizon import tabs
from horizon import tables
from horizon import workflows
import re

from a10_horizon.dashboard.api import scaling as api

import forms as project_forms
import tables as project_tables
import tabs as project_tabs
import workflows as project_workflows


LOG = logging.getLogger(__name__)

ACTION = "action"
NOUN = "noun"
PLURAL = "plural"

URL_PREFIX = "horizon:project:a10scaling:"


class IndexView(tabs.TabView):
    tab_group_class = (project_tabs.A10ScalingTabs)
    template_name = 'scaling_tabs.html'
    form_url = reverse_lazy(URL_PREFIX + "index")

    delete_actions = {
        "scalingpolicy": {
            ACTION: api.delete_a10_scaling_policy,
            NOUN: "Scaling Policy",
            PLURAL: "Scaling Policies",
        },
        "scalingaction": {
            ACTION: api.delete_a10_scaling_action,
            NOUN: "Scaling Action",
            PLURAL: "Scaling Actions",
        },
        "scalingalarm": {
            ACTION: api.delete_a10_scaling_alarm,
            NOUN: "Scaling Alarm",
            PLURAL: "Scaling Alarms",
        },
    }

    def post(self, request, *args, **kwargs):
        obj_ids = request.POST.getlist('object_ids')
        action = request.POST['action']
        m = re.search('.delete([a-z]+)', action).group(1)
        if obj_ids == []:
            obj_ids.append(re.search('([0-9a-z-]+)$', action).group(1))

        if m in self.delete_actions:
            delete_action = self.delete_actions[m]
            for obj_id in obj_ids:
                success_msg = "Deleted {0} {1}".format(delete_action[NOUN], obj_id)
                failure_msg = "Unable to delete {0} {1}".format(delete_action[NOUN], obj_id)

                try:
                    delete_action[ACTION](request, obj_id)
                    messages.success(request, success_msg)
                except Exception as ex:
                    exceptions.handle(request, failure_msg)
                    LOG.exception(ex)

        return self.get(request, *args, **kwargs)


class AddPolicyView(workflows.WorkflowView):
    name = _("Create Scaling Policy")
    workflow_class = project_workflows.AddPolicyWorkflow
    success_url = reverse_lazy(URL_PREFIX + "index")


class UpdatePolicyView(forms.views.ModalFormView):
    name = _("Update Scaling Policy")
    form_class = project_forms.UpdatePolicy
    context_object_name = "scaling_policy"
    success_url = reverse_lazy(URL_PREFIX + "index")
    template_name = "update.html"
    page_title = "Update Scaling Policy"

    def get_context_data(self, **kwargs):
        context = super(UpdatePolicyView, self).get_context_data(**kwargs)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        id = self.kwargs['scaling_policy_id']
        self.submit_url = reverse_lazy(URL_PREFIX + "updatescalingpolicy",
                                       kwargs={"scaling_policy_id": id})
        if id:
            try:
                return api.get_a10_scaling_policy(self.request, id)
            except Exception as ex:
                redirect = self.success_url
                msg = _("Unable to retrieve scaling policy: %s") % ex
                exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        rv = self._get_object()
        return rv


class PolicyDetailView(tables.MultiTableView):
    name = _("Update Policy Reactions")
    table_classes = (project_tables.UpdatePolicyReactionTable,)
    template_name = "detail.html"
    page_title = "Scaling Policy {{ scaling_policy.name }}"
    failure_url = URL_PREFIX + "index"

    def __init__(self, *args, **kwargs):
        super(PolicyDetailView, self).__init__(*args, **kwargs)

    # every table needs a get_<tablename>_data method
    def get_updatepolicyreactiontable_data(self):
        try:
            scaling_policy = self._get_data()
            reactions = scaling_policy["reactions"]
        except Exception as ex:
            LOG.exception(ex)
            redirect = self.failure_url
            msg = _("Unable to retrieve scaling policy reactions: %s") % exceptions
            exceptions.handle(self.request, msg, redirect=redirect)

        position = 0
        for reaction in reactions:
            reaction['position'] = position
            position += 1

        return reactions

    def _get_data(self):
        try:
            id = self.kwargs['scaling_policy_id']
            policy = api.get_a10_scaling_policy(self.request, id)
        except Exception:
            msg = _('Unable to retrieve details for scaling policy "%s".') \
                % (id)
            exceptions.handle(self.request, msg,
                              redirect=self.failure_url)
        return policy

    def get_context_data(self, **kwargs):
        context = super(PolicyDetailView, self).get_context_data(**kwargs)
        policy = self._get_data()

        context["scaling_policy"] = policy
        context["url"] = self.get_redirect_url()

        return context

    @staticmethod
    def get_redirect_url():
        return reverse_lazy("horizon:project:a10scaling:index")

    class Meta(object):
        name = "scalingpolicydetail"
        verbose_name = _("Scaling Policy Details")


class AddAlarmView(workflows.WorkflowView):
    name = _("Create Alarm")
    workflow_class = project_workflows.AddScalingAlarmWorkflow
    success_url = reverse_lazy("horizon:project:a10scaling:index")


class UpdateAlarmView(forms.views.ModalFormView):
    name = _("Update Alarm")
    title = name
    form_class = project_forms.UpdateAlarm
    context_object_name = "scaling_alarm"
    success_url = reverse_lazy(URL_PREFIX + "index")
    template_name = "alarm/update.html"
    page_title = "Update Alarm"

    def get_context_data(self, **kwargs):
        context = super(UpdateAlarmView, self).get_context_data(**kwargs)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        id = self.kwargs['id']
        self.submit_url = reverse_lazy(URL_PREFIX + "updatealarm",
                                       kwargs={"id": id})
        if id:
            try:
                return api.get_a10_scaling_alarm(self.request, id)
            except Exception as ex:
                msg = _("Unable to retrieve scaling alarm: %s") % ex
                exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        rv = self._get_object()
        return rv


class AddActionView(workflows.WorkflowView):
    name = _("Create Action")
    workflow_class = project_workflows.AddActionWorkflow
    success_url = reverse_lazy(URL_PREFIX + "index")


class UpdateActionView(forms.views.ModalFormView):
    name = _("Update Action")
    form_class = project_forms.UpdateAction
    context_object_name = "scaling_action"
    success_url = reverse_lazy(URL_PREFIX + "index")
    template_name = "action/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateActionView, self).get_context_data(**kwargs)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        id = self.kwargs['id']
        self.submit_url = reverse_lazy(URL_PREFIX + "updateaction",
                                       kwargs={"id": id})
        if id:
            try:
                return api.get_a10_scaling_action(self.request, id)
            except Exception as ex:
                msg = _("Unable to retrieve scaling action: %s") % ex
                exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        rv = self._get_object()
        return rv


class AddReactionView(workflows.WorkflowView):
    name = _("Create Reaction")
    workflow_class = project_workflows.AddReactionWorkflow
    success_url = reverse_lazy(URL_PREFIX + "index")
    template_name = "reaction/create.html"

    def get_context_data(self, **kwargs):
        return super(AddReactionView, self).get_context_data(**kwargs)

    def get_initial(self):
        self.submit_url = reverse_lazy(URL_PREFIX + "addreaction",
                                       kwargs=self.kwargs)
        return self.kwargs

    # def post(self, request, *args, **kwargs):
    #     return super(AddReactionView, self).post(request, *args, **kwargs)


class GroupDetailView(tables.MultiTableView):
    name = _("Scaling Group Overview")
    table_classes = (project_tables.A10ScalingGroupMemberTable,)
    template_name = "group/detail.html"
    page_title = "Scaling Group {{ scaling_group.name }}"
    failure_url = URL_PREFIX + "index"

    def __init__(self, *args, **kwargs):
        super(GroupDetailView, self).__init__(*args, **kwargs)

    # every table needs a get_<tablename>_data method
    def get_a10scalinggroupmembertable_data(self):
        try:
            group = self._get_data()
            workers = group.get("workers", [])

        except Exception as ex:
            LOG.exception(ex)
            redirect = self.failure_url
            msg = _("Unable to retrieve scaling group: %s") % exceptions
            exceptions.handle(self.request, msg, redirect=redirect)

        return workers

    def _get_data(self):
        try:
            id = self.kwargs['scaling_group_id']
            group = api.get_a10_scaling_group_with_children(self.request, id)
        except Exception:
            msg = _('Unable to retrieve details for scaling group "%s".') \
                % (id)
            exceptions.handle(self.request, msg,
                              redirect=self.failure_url)
        return group

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        group = self._get_data()

        context["scaling_group"] = group
        context["url"] = self.get_redirect_url()

        return context

    @staticmethod
    def get_redirect_url():
        # update redirect to go back to scaling group.
        return reverse_lazy("horizon:project:a10scaling:index")

    class Meta(object):
        name = "scalinggroupdetail"
        verbose_name = _("Scaling Group Details")
