# Copyright (C) 2016, A10 Networks Inc. All rights reserved.

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

import views

urlpatterns = patterns(

    'a10_horizon.dashboard.a10networks.a10scaling.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^addcertificate/$', views.AddCertificateView.as_view(),
        name='addcertificate'),
    url(r'^updatecertificate/(?P<certificate_id>[^/]+)/',
        views.UpdateCertificateView.as_view(), name='updatecertificate'),
    url(r'^addcertificatebinding/$', views.AddCertificateBindingView.as_view(),
        name="addcertificatebinding"),
)
