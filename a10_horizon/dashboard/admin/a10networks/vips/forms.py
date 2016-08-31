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

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

import forms as p_forms


# from openstack_dashboard import api
# lbaasv2 api
try:
    from neutron_lbaas_dashboard.api import lbaasv2 as lbaasv2_api
except ImportError as ex:
    LOG.exception(ex)
    LOG.warning("Could not import lbaasv2 dashboard API")


class EditVip(forms.SelfHandlingForm):
    def __init__(self, *args, **kwargs):
        super(EditVip, self).__init__(*args, **kwargs)
        self.submit_url = kwargs.get("id")

    id = forms.CharField(label=_("ID"), widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    description = forms.CharField(label=_("Description"), min_length=1,
                                  max_length=255, required=False)

    failure_url = "horizon:project:a10vips:index"
    success_url = "horizon:project:a10vips:index"
    # redirect_url = reverse_lazy('horizon:project:a10scaling:updatescalingpolicy')

    def handle(self, request, context):
        try:
            policy = lbaasv2_api.vip_update(request, **context)
            msg = _("VIP {0} was successfully updated").format(context["name"])
            messages.success(request, msg)
            return policy
        except Exception as ex:
            msg = _("Failed to update VIP %s") % context["name"]
            LOG.exception(ex)
            redirect = reverse_lazy(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
