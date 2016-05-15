# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.
from django.conf.urls import url
from django.conf.urls import include

import views
from a10scaling import urls as scaling_urls
from a10_horizon.dashboard.a10networks.a10devices import urls as device_urls

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^addcertificate/$', views.AddCertificateView.as_view(),
        name='addcertificate'),
    url(r'^updatecertificate/(?P<certificate_id>[^/]+)/',
        views.UpdateCertificateView.as_view(), name='updatecertificate'),
    url(r'^addcertificatebinding/$', views.AddCertificateBindingView.as_view(),
        name="addcertificatebinding"),
    url(r'^a10scaling/', include(scaling_urls, namespace="a10scaling")),
    url(r'^a10devices/', include(device_urls, namespace="a10devices"))
]
