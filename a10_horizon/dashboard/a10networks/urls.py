# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.
from django.conf.urls import url
from django.conf.urls import include

import views
from a10scaling import urls as scaling_urls


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^addcertificate/$', views.AddCertificateView.as_view(),
        name='addcertificate'),
    url(r'^updatecertificate/(?P<certificate_id>[^/]+)/',
        views.UpdateCertificateView.as_view(), name='updatecertificate'),
    url(r'^addcertificatebinding/$', views.AddCertificateBindingView.as_view(),
        name="addcertificatebinding"),
    url(r'^a10scaling/', include(scaling_urls, namespace="a10scaling"))
]
