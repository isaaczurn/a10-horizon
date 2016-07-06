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

urlpatterns = patterns("a10_horizon.dashboard.admin.a10networks.overview.views",
    url(r'^$', views.IndexView.as_view(), name='index'),
)


# urlpatterns = patterns("a10_horizon.dashboard.a10networks.a10scaling.views",
#                        url(r'^$',
#                            views.IndexView.as_view(),
#                            name='index'),
#                        url(r'^scalingpolicy/add$',
#                            views.AddPolicyView.as_view(),
#                            name='addscalingpolicy'),
#                        url(r'^scalingpolicy/update/(?P<scaling_policy_id>[^/]*)$',
#                            views.UpdatePolicyView.as_view(),
#                            name='updatescalingpolicy'),
#                        url(r'^scalingaction/add/$',
#                            views.AddActionView.as_view(),
#                            name='addaction'),
#                        url(r'^action/update/(?P<id>[^/]*)$',
#                            views.UpdateActionView.as_view(),
#                            name='updateaction'),
#                        url(r'^alarm/add/$',
#                            views.AddAlarmView.as_view(),
#                            name='addalarm'),
#                        url(r'^alarm/update/(?P<id>[^/]*)$',
#                            views.UpdateAlarmView.as_view(),
#                            name='updatealarm'),
#                        url(r'^scalingpolicy/(?P<scaling_policy_id>[^/]*)/addreaction$',
#                            views.AddReactionView.as_view(),
#                            name='addreaction'),
#                        url(r'^scalingpolicy/(?P<scaling_policy_id>[^/]*)/detail$',
#                            views.PolicyDetailView.as_view(),
#                            name='scalingpolicydetail'),
#                        url(r'^scalinggroup/(?P<scaling_group_id>[^/]*)/detail$',
#                            views.GroupDetailView.as_view(),
#                            name='scalinggroupdetail'))
