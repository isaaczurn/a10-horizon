# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.

import logging

from django.utils.translation import ugettext_lazy as _
from horizon import tabs
from horizon import exceptions

from a10_horizon.dashboard.api import scaling as scaling_api
import tables


LOG = logging.getLogger(__name__)


class A10ScalingGroupsTab(tabs.TableTab):
    table_classes = (tables.A10ScalingGroupTable,)
    name = _("Scaling Groups")
    slug = "a10scalinggroups"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_a10scalinggrouptable_data(self):
        try:
            rv = []
            tenant_id = self.request.user.tenant_id

            rv = scaling_api.get_a10_scaling_groups(self.tab_group.request,
                                                    tenant_id=tenant_id)
        except Exception as ex:
            rv = []
            errmsg = "Unable to retrieve scaling group list"
            exceptions.handle(self.tab_group.request, errmsg)
            LOG.exception(ex)

        return rv


class A10ScalingGroupMembersTab(tabs.TableTab):
    table_classes = (tables.A10ScalingGroupMemberTable,)
    name = _("Scaling Group Members")
    slug = "a10scalinggroupmembers"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_a10scalinggroupmemberstable_data(self):
        try:
            tenant_id = self.request.user.tenant_id
            rv = []
            rv = scaling_api.get_a10_scaling_group_members(self.tab_group.request,
                                                           tenant_id=tenant_id)
        except Exception as ex:
            rv = []
            LOG.exception(ex)
            errmsg = _("Unable to retrieve scaling group member list")
            exceptions.handle(self.tab_group.request, errmsg)

        return rv


class A10ScalingPoliciesTab(tabs.TableTab):
    table_classes = (tables.A10ScalingPolicyTable,)
    name = _("Scaling Group Policies")
    slug = "a10scalinggrouppolicies"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_a10scalingpolicytable_data(self):
        try:
            tenant_id = self.request.user.tenant_id
            rv = []
            rv = scaling_api.get_a10_scaling_policies(self.tab_group.request, tenant_id=tenant_id)
        except Exception as ex:
            rv = []
            LOG.exception(ex)
            errmsg = _("Unable to retrieve scaling policy list")
            exceptions.handle(self.tab_group.request, errmsg)

        return rv


class A10ScalingActionTab(tabs.TableTab):
    table_classes = (tables.A10ScalingActionTable,)
    name = _("Scaling Actions")
    slug = "a10scalingactions"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_a10scalingactiontable_data(self):
        try:
            tenant_id = self.request.user.tenant_id
            rv = []
            rv = scaling_api.get_a10_scaling_actions(self.tab_group.request, tenant_id=tenant_id)
        except Exception as ex:
            rv = []
            LOG.exception(ex)
            errmsg = _("Unable to retrieve scaling action list")
            exceptions.handle(self.tab_group.request, errmsg)

        return rv


class A10ScalingAlarmTab(tabs.TableTab):
    table_classes = (tables.A10ScalingAlarmTable,)
    name = _("Scaling Alarms")
    slug = "a10scalingalarms"
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_a10scalingalarmtable_data(self):
        try:
            tenant_id = self.request.user.tenant_id
            rv = []
            rv = scaling_api.get_a10_scaling_alarms(self.tab_group.request, tenant_id=tenant_id)
        except Exception as ex:
            rv = []
            LOG.exception(ex)
            errmsg = _("Unable to retrieve scaling alarm list")
            exceptions.handle(self.tab_group.request, errmsg)

        return rv


class A10ScalingTabs(tabs.TabGroup):
    slug = "a10scalingtabs"
    tabs = (A10ScalingGroupsTab,
            A10ScalingPoliciesTab,
            A10ScalingActionTab,
            A10ScalingAlarmTab)
    sticky = True
