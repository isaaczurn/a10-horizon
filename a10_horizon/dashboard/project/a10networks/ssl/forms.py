# Copyright (C) 2016, A10 Networks Inc. All rights reserved.

import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

# from openstack_dashboard import api
from a10_horizon.dashboard.api import certificates as api

LOG = logging.getLogger(__name__)


class UpdateCertificate(forms.SelfHandlingForm):
    id = forms.CharField(label=_("ID"), widget=forms.TextInput(
                         attrs={'readonly': 'readonly'}))
    name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    description = forms.CharField(label=_("Description"), min_length=1,
                                  max_length=255, required=True)
    cert_data = forms.CharField(label=_("Data"), min_length=1, max_length=1024,
                                required=True)
    key_data = forms.CharField(
        label=_("Key Data"), min_length=1, max_length=8000,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 15}), required=True)
    password = forms.CharField(
        label=_("Password"), min_length=1, max_length=1024,
        widget=forms.PasswordInput(render_value=False), required=False)
    intermediate_data = forms.CharField(
        label=_("Intermediate Certificate Data"), min_length=1, max_length=8000,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 15}), required=False)

    failure_url = 'horizon:project:a10ssl:index'

    def handle(self, request, context):
        LOG.debug("UpdateCertificate:handle(): context" % context)
        try:
            certificate = api.certificate_update(request, **context)
            msg = _('Certificate {0} was successfully updated.').format(context['id'])
            LOG.debug(msg)
            messages.success(request, msg)
            return certificate
        except Exception:
            msg = _('Failed to update certificate %s') % context['id']
            LOG.exception(msg)
            redirect = reverse(self.failure_url)
            exceptions.handle(request, msg, redirect=redirect)
