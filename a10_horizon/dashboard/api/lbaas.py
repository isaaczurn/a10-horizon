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


LOG = logging.getLogger(__name__)


class LoadBalancer(NeutronAPIDictWrapper):
    """Wrapper for LBaaSv2 Load Balancer"""
    def __init__(self, apiresource):
        super(LoadBalancer, self).__init__(apiresource)


class Listener(NeutronAPIDictWrapper):
    """Wrapper for LBaaSv2 Listener"""
    def __init__(self, apiresource):
        super(Listener, self).__init__(apiresource)


class Member(NeutronAPIDictWrapper):
    """Wrapper for LBaaSv2 Member"""
    def __init__(self, apiresource):
        super(Member, self).__init__(apiresource)


class HealthMonitor(NeutronAPIDictWrapper):
    """Wrapper for LBaaSv2 Health Monitor"""
    def __init__(self, apiresource):
        super(HealthMonitor, self).__init__(apiresource)


class Pool(NeutronAPIDictWrapper):
    """Wrapper for LBaaSv2 Pool"""
    def __init__(self, apiresource):
        super(Pool, self).__init__(apiresource)


class L7Policy(NeutronAPIDictWrapper):
    """Wrapper for LBaaSv2 L7 Policy"""
    def __init__(self, apiresource):
        super(L7Policy, self).__init__(apiresource)


class L7Rule(NeutronAPIDictWrapper):
    """Wrapper for LBaaSv2 L7 Rule"""
    def __init__(self, apiresource):
        super(L7Rule, self).__init__(apiresource)


def list_loadbalancers(request, **kwargs):
    rv = neutronclient(request).list_loadbalancers(**kwargs).get("loadbalancers")
    return map(LoadBalancer, rv)


def get_loadbalancer(request, id, **params):
    rv = neutronclient(request).show_loadbalancer(id).get("loadbalancer")
    return LoadBalancer(rv)


def delete_loadbalancer(request, id):
    neutronclient(request).delete_loadbalancer(id)


def create_loadbalancer(request, **kwargs):
    body = {"loadbalancer": kwargs}
    rv = neutronclient(request).create_loadbalancer(body=body).get("loadbalancer")
    return LoadBalancer(rv)


def update_loadbalancer(request, id, **kwargs):
    body = {"loadbalancer": kwargs}
    rv = neutronclient(request).update_loadbalancer(id, body=body).get("loadbalancer")
    return LoadBalancer(rv)
