
from openstack_dashboard.api import nova as nova_api
import openstack_dashboard.api.keystone as keystone_api
import openstack_dashboard.api.glance as glance_api

def get_result(request, results):
    servers = nova_api.server_list(request) #get list of servers
    server_ids = [x["nova_instance_id"] for x in results] #get list of nova id's from results
    instance_servers = [x for x in servers if x.id in server_ids] # get servers if server id is in results
    flavors = novaclient.server_list(request)
    server_flavors = [x["flavor"] for x in instance_servers]
    instance_flavors = [x for x in flavors if x.id in server_flavors]
    tenants= keystone_api.tenant_list(request)

    for instance in results:
        for server in instance_servers:
            if instance["nova_instance_id"] == server.id:
                for flavor in instance_flavors:
                    if server["flavor"].id == flavor.id:
                        instance["flavor"] = flavor
                            
                for tenant in tenants:
                    if server["tenant_id"] == tenant.id:
                        instance["owner"] = tenant.name

                    
                instance["image"] = glance_api.image_get(request, server["image"].id)

    return results

def migrate(request, id, host):
    nova_api.server_live_migrate(request, id, host)
