# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf import settings
from django.conf.urls import static

import a10_horizon
from a10devices import urls as device_urls
from a10scaling import urls as scaling_urls
from a10ssl import urls as ssl_urls
import views


urlpatterns = patterns("",
    url(r'^a10networks/', views.IndexView.as_view(), name='index'),
    url(r'^a10ssl/', include(ssl_urls, app_namesppace="a10networks", namespace="a10ssl")),
    url(r'^a10scaling/', include(scaling_urls, app_namesppace="a10networks", namespace="a10scaling")),
    url(r'^a10devices/', include(device_urls, app_namesppace="a10networks", namespace="a10devices"))
)
