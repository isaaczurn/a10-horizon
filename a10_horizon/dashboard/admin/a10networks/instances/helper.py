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

import openstack_dashboard.api.keystone as keystone_api
import openstack_dashboard.api.glance as glance_api
import openstack_dashboard.api.nova as nova_api

LOG = logging.getLogger(__name__)

def get_hosts(request, filter=None):
    hyper_list = nova_api.hypervisor_list(request)
    for elem in hyper_list:
        if elem.hypervisor_hostname == filter:
            return elem.id

    host_list = []
    for hyper in hyper_list:
        host_list.append(hyper.host_ip)

    return host_list

def get_result(request, results):
    if len(results) > 0:
        servers = nova_api.server_list(request) #get list of servers
        server_ids = [x["nova_instance_id"] for x in results] #get list of nova id's from results

    result_list = []
    for instance in results:
        server = nova_api.server_get(request, instance["nova_instance_id"])
        flavor = server.flavor
        flavor_id = flavor["id"]

        tenants = keystone_api.tenant_list(request)

        setattr(instance, "flavor", nova_api.flavor_get(request, flavor_id))
        setattr(instance, "image", server.image_name)
        setattr(instance, "owner", keystone_api.tenant_get(request, server.tenant_id).name)
        setattr(instance, "comp_name", server.host_server)
        setattr(instance, "comp_id", get_hosts(request, server.host_server))
        result_list.append(instance)
    return result_list

def migrate(request, id, host):
    try:
        nova_api.server_live_migrate(request, id, host)
    except Exception:
        LOG.exception("Failure to migrate.")
        return results

def migrate(request, id, host):
    nova_api.server_live_migrate(request, id, host)

def get_hosts(request):
    host_list = nova_api.host_list(request)
    if host_list:
       return host_list
    return ["192.168.1.0"]
