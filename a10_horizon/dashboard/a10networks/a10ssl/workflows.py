# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.

import logging

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import workflows

# a10_horizon.dashboard.api.client.Client extends neutron.api.client.Client
from a10_horizon.dashboard.api import certificates as api
from openstack_dashboard.api import lbaas as lbaas_api

# TODO(Pull these from A10 constants)
AVAILABLE_PROTOCOLS = ('HTTP', 'HTTPS', 'TCP')
AVAILABLE_METHODS = ('ROUND_ROBIN', 'LEAST_CONNECTIONS', 'SOURCE_IP')

LOG = logging.getLogger(__name__)


class AddCertificateAction(workflows.Action):
    name = forms.CharField(label=_("Name"), min_length=1, max_length=255,
                           required=True)
    description = forms.CharField(label=_("Description"), min_length=1,
                                  max_length=255, required=False)
    cert_data = forms.CharField(
        label=_("Certificate Data"), min_length=1, max_length=8000,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 15}), required=True)
    key_data = forms.CharField(
        label=_("Key Data"), min_length=1, max_length=8000,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 15}), required=True)
    password = forms.CharField(
        label=_("Password"), min_length=1, max_length=1024,
        widget=forms.PasswordInput(render_value=False), required=False)
    intermediate_data = forms.CharField(
        label=_("Intermediate Certificate Data"), min_length=1, max_length=8000,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 15}), required=False)

    def clean(self):
        cleaned_data = super(AddCertificateAction, self).clean()
        LOG.debug("AddCertificateAction:clean(): cleaned_data=%s" % cleaned_data)
        file = cleaned_data.get('cert_file')
        data = cleaned_data.get('cert_data')
        LOG.info("file: {}".format(file))
        LOG.info("data: {}".format(data))
        LOG.info("self.files: {}".format(self.files))
        LOG.info("self.request.FILES: {}".format(self.request.FILES.keys()))
        if file and data:
            msg = _("You may only enter certificate data if you are not uploading the certificate.")
            self._errors['cert_data'] = self.error_class([msg])
        return cleaned_data

    class Meta(object):
        name = _("Add New Certificate")
        permissions = ('openstack.services.network',)
        help_text = _("Add a certificate.\n\n Something about using a file or "
                      "copy-pasta.")  # FIXME(traff)


class AddCertificateStep(workflows.Step):
    action_class = AddCertificateAction
    contributes = ("name", "description", "cert_data",
                   "key_data", "intermediate_data", "password")


class AddCertificate(workflows.Workflow):
    slug = "addcertificate"
    name = _("Add Certificate")
    finalize_button_name = _("Add")
    success_message = _('Added certificate')
    failure_message = _('Unable to add certificate')
    success_url = "horizon:project:a10ssl:index"
    default_steps = (AddCertificateStep,)

    def handle(self, request, context):
        try:
            LOG.debug("AddCertificate:handle(): context=%s" % (context))
            context['certificate_id'] = api.certificate_create(
                request, **context).get('id')
            return True
        except Exception as ex:
            LOG.error("Could not add certificate. ERROR=%s" % ex)
            exceptions.handle(request, _("Unable to add certificate."))
        return False


class AddCertificateBindingAction(workflows.Action):
    vip_id = forms.ChoiceField(label=_("VIP"))
    certificate_id = forms.ChoiceField(label=_("Certificate"))

    def __init__(self, request, *args, **kwargs):
        certificates = []
        vips = []
        super(AddCertificateBindingAction, self).__init__(request, *args, **kwargs)

        tenant_id = request.user.tenant_id

        vip_id_choices = [('', _("Select a VIP"))]
        certificate_id_choices = [('', _("Select a Certificate"))]

        try:
            kwargs["tenant_id"] = tenant_id
            vips = lbaas_api.vip_list(request, **kwargs)
        except Exception as ex:
            LOG.error("Could not add certificate. ERROR=%s" % ex)
            exceptions.handle(request, _("Unable to retrieve VIPs list"))

        try:
            certificates = api.certificate_list(request, **kwargs)
        # TODO(mdurrant) narrow exception handling
        except Exception as ex:
            LOG.error("Could retrieve certificate list. ERROR=%s" % ex)
            exceptions.handle(request, _("Unable to retrieve Certificates"))

        for v in vips:
            # we only care about HTTPS connections
            if (v.protocol == "HTTPS"):
                vip_id_choices.append((v.id, v.name))

        for c in certificates:
            certificate_id_choices.append((c.id, c.name))

        self.fields['vip_id'].choices = vip_id_choices
        self.fields['certificate_id'].choices = certificate_id_choices

    def clean(self):
        cleaned_data = super(AddCertificateBindingAction, self).clean()
        # TODO(mdurrant): Not sure there's any sanitation to be performed here
        return cleaned_data

    class Meta(object):
        name = _("Add New Certificate Association")
        # FIXME(mdurrant) - API policy covers these but we should probably double-check
        permissions = ('openstack.services.network',)
        help_text = _("Assign a Certificate to VIP\n\n")


class AddCertificateBindingStep(workflows.Step):
    action_class = AddCertificateBindingAction
    contributes = ("vip_id", "certificate_id")


class AddCertificateBinding(workflows.Workflow):
    slug = "addcertificatebinding"
    name = _("Add VIP Association")
    finalize_button_name = ("Create Association")
    success_message = _("Added association between VIP:'%s' and Certificate:'%s'.")  # noqa
    failure_message = _("Unable to create association for VIP:'%s',Certificate:'%s'")  # noqa
    default_steps = (AddCertificateBindingStep,)
    success_url = "horizon:project:a10ssl:index"

    def format_status_message(self, message):
        vip_id = self.context.get('vip_id')
        certificate_id = self.context.get('certificate_id')
        return message % (vip_id, certificate_id)

    def handle(self, request, context):
        # make sure they both exist.
        try:
            api.certificate_binding_create(request, **context)
            return True
        # TODO(mdurrant) narrow exception handling
        except Exception as ex:
            LOG.error("Could not add certificate association. ERROR=%s" % ex)
            return False
