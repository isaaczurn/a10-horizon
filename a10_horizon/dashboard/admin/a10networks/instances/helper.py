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

def get_result(request, results):
#    import pdb; pdb.set_trace()
    if len(results) > 0:
        servers = nova_api.server_list(request) #get list of servers
        server_ids = [x["nova_instance_id"] for x in results] #get list of nova id's from results
#        LOG.info("SERVER_ID")
#        LOG.info(servers)
#        LOG.info(servers["servers"])
#        instance_server_ids = []
#        for x in servers["servers"]:
#            if x["id"] in server_ids:
#                instance_server_ids.append(x["id"])       
        #instance_servers = [nova_api.server_get(request, x) for x in instance_server_ids] # list of full server object dictionaries
        #flavors = nova_api.flavor_list(request)
        #server_flavors = [x["flavor"] for x in instance_servers] # should be a list of flavor dictionaries
        #instance_flavors = [x for x in flavors["flavors"] if x["id"] in server_flavors]
        #tenants= keystone_api.tenant_list(request)

#        for instance in results:
#            for server in instance_servers:
#                if instance["nova_instance_id"] == server["id"]:
#                    for flavor in instance_flavors:
#                        if server["flavor"]["id"] == flavor["id"]:
#                            instance["flavor"] = flavor
#
#                    for tenant in tenants:
#                        if server["tenant_id"] == tenant["id"]:
#                            instance["owner"] = tenant["name"]
#
#                    instance["image"] = glance_api.image_get(request, server["image"]["id"])
#
    return results

def migrate(request, id, host):
    try:
        nova_api.server_live_migrate(request, id, host)
    except Exception:
        LOG.exception("Failure to migrate.")

def get_hosts(request):
    hyper_list = nova_api.hypervisor_list(request)
    host_list = []
    for hyper in hyper_list:
        host_list.append(hyper.host_ip)

    if host_list:
       return host_list
