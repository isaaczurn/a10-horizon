# Copyright (C) 2016, A10 Networks Inc. All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf import settings
from django.conf.urls import static

import a10_horizon
import views

urlpatterns = patterns("a10_horizon.dashboard.admin.a10networks.instances.views",
    url(r'a10deviceinstances$', views.IndexView.as_view(), name='index'),
)
