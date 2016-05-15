# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.

import logging

from django.utils.translation import ugettext_lazy as _

from a10_neutron_lbaas import a10_config
from horizon import tabs
from horizon import exceptions

import tables
from a10_horizon.dashboard.api import certificates as cert_api


LOG = LOG = logging.getLogger(__name__)


class CertificatesTab(tabs.TableTab):
    table_classes = (tables.CertificatesTable,)
    name = _("Certificates")
    slug = "certificates"
    template_name = "certificates/_certificates_tab.html"
    preload = False

    def get_certificatestable_data(self):
        try:
            tenant_id = self.request.user.tenant_id
            certificates = []
            certificates = cert_api.certificate_list(self.tab_group.request,
                                                     tenant_id=tenant_id)
        except Exception as ex:
            certificates = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve certificate list.'))
            LOG.error("Could not retrieve certificate list. ERROR=%s" % ex)
        return certificates


class CertificateBindingsTab(tabs.TableTab):
    table_classes = (tables.CertificateBindingsTable,)
    name = _("Certificate Associations")
    slug = "certificatebindings"
    template_name = "certificates/_certificatebindings_tab.html"

    def get_certificatebindingtable_data(self):
        try:
            tenant_id = self.request.user.tenant_id
            bindings = []
            bindings = cert_api.certificate_bindings_list(self.tab_group.request,
                                                          tenant_id=tenant_id)
        except Exception as ex:
            bindings = []
            exceptions.handle(self.tab_group.request, _("Unable to retrieve certificate "
                                                        "associations list."))
            LOG.error("Could not retrieve certificate associations list. ERROR=%s" % ex)

        return bindings


class A10SSLTabs(tabs.TabGroup):
    slug = "a10ssltabs"
    tabs = (CertificatesTab,
            CertificateBindingsTab
            )
    sticky = True
