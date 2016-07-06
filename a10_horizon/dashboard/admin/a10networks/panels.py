# Copyright 2015,  A10 Networks
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

from django.utils.translation import ugettext_lazy as _

from a10_horizon.dashboard.panel_base import NeutronExtensionPanelBase


LOG = logging.getLogger(__name__)

# TODO(mdurrant) Move these in to a single module for easy reference/update
ADMIN_PERMISSIONS = ('openstack.services.network',)


class A10OverviewAdminPanel(NeutronExtensionPanelBase):

    name = "Overview"
    slug = "a10overview_admin"
    permissions = ADMIN_PERMISSIONS


class A10DeviceInstancesAdminPanel(NeutronExtensionPanelBase):
    # REQUIRED_EXTENSIONS = ["a10-device-instance"]

    name = "LB Device Instances"
    slug = "a10deviceinstances_admin"
    permissions = ADMIN_PERMISSIONS


class A10VipsAdminPanel(NeutronExtensionPanelBase):
    # REQUIRED_EXTENSIOSN = ["a10-scaling-groups"]

    name = "VIPs"
    slug = "a10vips_admin"
    permissions = ADMIN_PERMISSIONS


class A10ScalingGroupsAdminPanel(NeutronExtensionPanelBase):

    name = "Scaling Groups"
    slug = "a10scalinggroups_admin"
    permissions = ADMIN_PERMISSIONS
