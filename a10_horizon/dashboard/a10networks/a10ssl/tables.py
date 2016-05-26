# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.

import logging

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import tables

LOG = logging.getLogger(__name__)


class AddCertificateLink(tables.LinkAction):
    name = "addcertificate"
    verbose_name = _("Add Certificate")
    url = "horizon:project:a10ssl:addcertificate"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "create_certificate"),)  # FIXME(traff)


class DeleteCertificateLink(tables.DeleteAction):
    name = "deletecertificate"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of %(data_type)s")
    data_type_singular = _("Certificate")
    data_type_plural = _("Certificates")

    # def allowed(self, request, datum=None):
    #     is_allowed = (datum and datum.id)
    #     LOG.debug("DeleteCertificateLink:allowed(): datum=%s,is_allowed=%s" % (datum, is_allowed))
    #     return True


class DeleteCertificateBindingLink(tables.DeleteAction):
    name = "deletecertificatebinding"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of %(data_type)s")
    data_type_singular = _("Certificate Association")
    data_type_plural = _("Certificate Associations")

    # def allowed(self, request, datum=None):
    #     is_allowed = (datum and datum.id)
    #     LOG.debug("DeleteCertificateBindingLink:allowed(): datum=%s,is_allowed=%s").format(
    #         datum, is_allowed)
    #     return True


class AddCertificateBindingLink(tables.LinkAction):
    name = "addcertificatebinding"
    verbose_name = _("Add Certificate Association")
    url = "horizon:project:a10ssl:addcertificatebinding"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "create_certificate_binding"),)  # FIXME(traff)


class UpdateCertificateLink(tables.LinkAction):
    name = "updatecertificate"
    verbose_name = _("Edit Certificate")
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, certificate):
        base_url = reverse_lazy("horizon:project:a10ssl:updatecertificate",
                                kwargs={'certificate_id': certificate.id})
        return base_url


class CertificatesTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    name = tables.Column("name", verbose_name=_("Name"))
    description = tables.Column("description", verbose_name=_("Description"))

    class Meta(object):
        name = "certificatestable"
        verbose_name = _("Certificates")
        table_actions = (AddCertificateLink, DeleteCertificateLink)
        row_actions = (UpdateCertificateLink, )


class CertificateBindingsTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    vip_id = tables.Column("vip_id", verbose_name=_("VIP ID"), hidden=True)
    certificate_id = tables.Column("certificate_id", verbose_name=_("Certificate ID"), hidden=True)
    vip_name = tables.Column("vip_name", verbose_name=_("VIP"))
    certificate_name = tables.Column("certificate_name", verbose_name=_("Certificate"))

    class Meta(object):
        name = "certificatebindingtable"
        verbose_name = _("Certificate Associations")
        table_actions = (AddCertificateBindingLink, DeleteCertificateBindingLink)
        row_actions = ()
