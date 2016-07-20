 # Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf import settings
from django.conf.urls import static

import a10_horizon
from instances import urls as instances_urls
from overview import urls as overview_urls
from vips import urls as vips_urls
# from a10scaling import urls as scaling_urls
# from a10ssl import urls as ssl_urls
import views

APP_NAMESPACE="a10networks"

urlpatterns = patterns("",
    url(r'^/', views.IndexView.as_view(), name='index'),
    url(r'^/ssl/', include(ssl_urls, APP_NAMESPACE, "a10ssl")),
    url(r'^/scaling/',
        include(scaling_urls, APP_NAMESPACE, "a10scaling")),
    url(r'^/instances/',
        include((instances_urls, APP_NAMESPACE, "a10instances")),
    url(r'^/overview',
        include(overview_urls, APP_NAMESPACE, "a10overview")),
    url(r'^/vips',
        include(vips_urls, APP_NAMESPACE, "a10vips"))

)
