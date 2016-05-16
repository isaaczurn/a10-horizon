# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from horizon import messages
from horizon import tabs
from horizon import workflows
import logging

from a10_horizon.dashboard.api import certificates as cert_api
import forms as project_forms
import workflows as project_workflows
import tabs as project_tabs

import re

LOG = logging.getLogger(__name__)


ACTION = "action"
NOUN = "noun"
PLURAL = "plural"


class IndexView(tabs.TabView):
    tab_group_class = (project_tabs.A10SSLTabs)
    template_name = 'ssl_tabs.html'

    delete_actions = {
        "certificate": {
            ACTION: cert_api.certificate_delete,
            NOUN: "Certificate",
            PLURAL: "Certificates"
        },
        "certificatebinding": {
            ACTION: cert_api.certificate_binding_delete,
            NOUN: "Certificate Association",
            PLURAL: "Certificate Associations"
        },
    }

    def post(self, request, *args, **kwargs):
        obj_ids = request.POST.getlist('object_ids')
        action = request.POST['action']
        m = re.search('.delete([a-z]+)', action).group(1)
        if obj_ids == []:
            obj_ids.append(re.search('([0-9a-z-]+)$', action).group(1))

        if m in self.delete_actions:
            delete_action = self.delete_actions[m]
            for obj_id in obj_ids:
                success_msg = "Deleted {0} {1}".format(delete_action[NOUN], obj_id)
                failure_msg = "Unable to delete {0} {1}".format(delete_action[NOUN], obj_id)

                try:
                    delete_action[ACTION](request, obj_id)
                    messages.success(request, success_msg)
                except Exception as ex:
                    exceptions.handle(request, failure_msg)
                    LOG.exception(ex)

        return self.get(request, *args, **kwargs)


class AddCertificateView(workflows.WorkflowView):
    workflow_class = project_workflows.AddCertificate


class AddCertificateBindingView(workflows.WorkflowView):
    workflow_class = project_workflows.AddCertificateBinding


class UpdateCertificateView(forms.ModalFormView):
    form_class = project_forms.UpdateCertificate
    template_name = "certificates/updatecertificate.html"
    context_object_name = 'certificate'
    success_url = reverse_lazy("horizon:project:a10ssl:index")

    def get_context_data(self, **kwargs):
        context = super(UpdateCertificateView, self).get_context_data(**kwargs)
        context["certificate_id"] = self.kwargs['certificate_id']
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        certificate_id = self.kwargs['certificate_id']
        try:
            return cert_api.certificate_get(self.request, certificate_id)
        except Exception as e:
            redirect = self.success_url
            msg = _('Unable to retrieve certificate. %s') % e
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        certificate = self._get_object()  # FIXME(traff)
        # return {'certificate_id': certificate['id'], 'name': 'hello_world',
        return certificate
