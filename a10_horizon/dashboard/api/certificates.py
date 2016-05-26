# Copyright (C) 2015 A10 Networks Inc. All rights reserved.

from __future__ import absolute_import

import logging

from django.conf import settings

from horizon.utils.memoized import memoized  # noqa

from openstack_dashboard.api import base

from openstack_dashboard.api.neutron import NeutronAPIDictWrapper
# a10 client that extends neutronclient.v2_0.client.Client
from a10_openstack.neutron_ext.api import client as neutron_client

LOG = logging.getLogger(__name__)


class Certificate(NeutronAPIDictWrapper):
    """Wrapper for neutron Certificates"""
    def __init__(self, apiresource):
        super(Certificate, self).__init__(apiresource)


class CertificateBinding(NeutronAPIDictWrapper):
    """Wrapper for neutron CertificateBindings"""
    def __init__(self, apiresource):
        super(CertificateBinding, self).__init__(apiresource)


def neutronclient(request):
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    LOG.debug('neutronclient connection created using token "%s" and url "%s"'
              % (request.user.token.id, base.url_for(request, 'network')))
    LOG.debug('user_id=%(user)s, tenant_id=%(tenant)s' %
              {'user': request.user.id, 'tenant': request.user.tenant_id})
    c = neutron_client.Client(token=request.user.token.id,
                              auth_url=base.url_for(request, 'identity'),
                              endpoint_url=base.url_for(request, 'network'),
                              insecure=insecure,
                              ca_cert=cacert)
    return c


def certificate_list(request, **params):
    LOG.debug("certificates_list(): params=%s" % (params))
    certificates = []
    certificates = neutronclient(request).list_certificates(**params).get('certificates')
    return map(Certificate, certificates)


def certificate_get(request, certificate_id, **params):
    # TODO(mdurrant): Add option to get bindings w/ cert.
    LOG.debug("certificate_get(): certificate_id=%s, params=%s" % (certificate_id, params))
    certificate = neutronclient(request).show_certificate(certificate_id,
                                                          **params).get('certificate')
    return Certificate(certificate)


def certificate_create(request, **kwargs):
    """Create specified Certificate"""
    body = {"certificate": kwargs}
    LOG.debug("certificate_create(): kwargs=%s,body=%s" % (kwargs, body))
    certificate = neutronclient(request).create_certificate(body=body).get('certificate')
    return Certificate(certificate)


def certificate_update(request, **kwargs):
    body = {"certificate": kwargs}
    LOG.debug("certificate_update(): kwargs=%s", (kwargs))
    certificate = neutronclient(request).update_certificate(body=body).get('certificate')
    return Certificate(certificate)


def certificate_delete(request, certificate_id):
    LOG.debug("certificate_delete(): certificiate_id:%s" % certificate_id)
    # TODO(mmd): Should this return status or do we assume it always works?
    neutronclient(request).delete_certificate(certificate_id)


def certificate_bindings_list(request, **params):
    LOG.debug("certificate_bindings_list(): params={}".format(params))

    bindings = \
        neutronclient(request).list_certificate_bindings(**params).get('certificate_bindings')
    return map(CertificateBinding, bindings)


def certificate_binding_get(request, binding_id, **params):
    LOG.debug("certificate_binding_get(): binding_id=%s, params=%s" % (binding_id, params))
    binding = neutronclient(request).show_certificate_binding(binding_id,
                                                              **params).get('certificate_binding')
    return CertificateBinding(binding)


def certificate_binding_create(request, **kwargs):
    """Binding specified Certificate ID to specified VIP ID"""
    LOG.debug("certificate_binding_create(): request=%s, kwargs=%s" % (request, kwargs))
    body = {'certificate_binding': kwargs}

    binding = \
        neutronclient(request).create_certificate_binding(body=body).get('certificate_binding')
    return CertificateBinding(binding)


def certificate_binding_delete(request, binding_id):
    LOG.debug("certificate_binding_delete(): binding_id=%s" % binding_id)
    neutronclient(request).delete_certificate_binding(binding_id)
