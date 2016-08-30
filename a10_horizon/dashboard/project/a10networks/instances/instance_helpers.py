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

from copy import copy

from keystoneclient.auth.identity import generic as auth_plugin
from keystoneclient import session as keystone_session
from openstack_dashboard.api import base

from a10_neutron_lbaas.vthunder import instance_manager
from a10_neutron_lbaas.vthunder import keystone


def url_for(request):
    return base.url_for(request, "identity")

# def token_for(request):
#     auth_url = base.url_for(request, 'identity')
#     auth_token = request.user.token.unscoped_token
#     project_name = request.user.token.project["name"]
#     return auth_plugin.Token(token=auth_token,
#                              project_name=project_name,
#                              auth_url=auth_url)


# def session_for(request):
#     token = token_for(request)
#     session = keystone_session.Session(auth=token)
#     return session


# def project_id_for(request):
#     return request.user.token.project["id"]


# def instance_manager_for(request):
#     return instance_manager.InstanceManager(session_for(request))


def instance_manager_from_context(config, context):
    ks = keystone.KeystoneFromHorizonRequest(config, context)
    nova_version = config.get('nova_api_version')
    return instance_manager.InstanceManager(ks_session=ks.session,
                                            nova_version=nova_version)


def config_from_context(context):
    networks = [context["mgmt_network"]]
    for x in context.get("data_networks", []):
        networks.append(x)

    return {
        "name": context.get("name"),
        "networks": [x for x in networks]
    }


def record_from_instance(instance):
    rv = copy.copy(instance_manager._default_server)
    rv.update(instance)
    return rv


def default_config(request):
    return {
        "keystone_version": 3,
        "keystone_auth_url": url_for(request),
        "nova_api_version": "2.1",
        'username': 'admin',
        'password': 'a10',
        "glance_image": "acos4.1.1",
        "nova_flavor": "vthunder.small",
    }
