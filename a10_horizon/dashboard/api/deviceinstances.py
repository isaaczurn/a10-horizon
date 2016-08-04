# Copyright (C) 2015 A10 Networks Inc. All rights reserved.
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

from __future__ import absolute_import

import logging
from openstack_dashboard.api.neutron import NeutronAPIDictWrapper
from openstack_dashboard.api.neutron import neutronclient

from a10_openstack_lib.resources import a10_device_instance

LOG = logging.getLogger(__name__)


class A10DeviceInstance(NeutronAPIDictWrapper):
    """Wrapper for a10_appliance dictionary"""
    def __init__(self, apiresource):
        super(A10DeviceInstance, self).__init__(apiresource)


def get_a10_device_instances(request, **kwargs):
    rv = neutronclient(request).list_a10_device_instances(**kwargs).get(a10_device_instance.RESOURCES)
    return map(A10DeviceInstance, rv)


def get_a10_device_instance(request, id, **params):
    rv = neutronclient(request).show_a10_device_instance(id).get(a10_device_instance.RESOURCE)
    return A10DeviceInstance(rv)


def delete_a10_device_instance(request, id):
    neutronclient(request).delete_a10_device_instance(id)


def create_a10_device_instance(request, **kwargs):
    body = {a10_device_instance.RESOURCE: kwargs}
    rv = neutronclient(request).create_a10_device_instance(body=body).get(a10_device_instance.RESOURCE)
    return A10DeviceInstance(rv)


def update_a10_device_instance(request, id, **kwargs):
    body = {a10_device_instance.RESOURCE: kwargs}
    rv = neutronclient(request).update_a10_device_instance(id, body=body).get(a10_device_instance.RESOURCE)
    return A10DeviceInstance(rv)
