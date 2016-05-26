# Copyright 2015 A10 Networks
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
import uuid

from django.utils.translation import ugettext_lazy as _

import horizon.forms as forms
import horizon.tables as tables
import horizon.workflows as workflows
import openstack_dashboard.api.glance as glance_api
import openstack_dashboard.api.neutron as neutron_api
import openstack_dashboard.api.nova as nova_api


GLANCE_API_VERSION_LIST = 2
GLANCE_API_VERSION_CREATE = 2
GLANCE_API_VERSION_UPDATE = 1

LOG = logging.getLogger(__name__)

