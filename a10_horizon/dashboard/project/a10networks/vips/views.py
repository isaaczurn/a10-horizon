# Copyright (C) 2016, A10 Networks Inc. All rights reserved.
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
import re

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from horizon import messages
from horizon import tabs
from horizon import views
from horizon import workflows

# lbaasv2 api
try:
    from neutron_lbaas_dashboard.api import lbaasv2 as lbaasv2_api
except ImportError as ex:
    LOG.exception(ex)
    LOG.warning("Could not import lbaasv2 dashboard API")

import forms as p_forms
import tabs as p_tabs


LOG = logging.getLogger(__name__)
URL_PREFIX = "horizon:project:a10vips:"

class IndexView(tabs.TabView):
    template_name = "vips/vip_tabs.html"
    tab_group_class = p_tabs.VipTabs
    page_title = "VIPs"


class EditVipView(forms.views.ModalFormView):
    name = _("Edit VIP")
    form_class = p_forms.EditVip
    context_object_name = "vip"
    success_url = reverse_lazy(URL_PREFIX + "index")
    template_name = "vips/update.html"
    page_title = name

    def get_context_data(self, **kwargs):
        context = super(EditVipView, self).get_context_data(**kwargs)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        id = self.kwargs['id']
        self.submit_url = reverse_lazy(URL_PREFIX + "edit",
                                       kwargs={"id": id})
        if id:
            try:
                rv = lbaasv2_api.show_loadbalancer(self.request, id)
                LOG.info(rv)
                return rv
            except Exception as ex:
                redirect = self.success_url
                msg = _("Unable to retrieve VIP: %s") % ex
                exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        rv = self._get_object()
        return rv
