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
)
