# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.
from django.conf.urls import patterns
from django.conf.urls import url

from a10_horizon.dashboard.a10networks.a10scaling import views

# TODO(mdurrant): Create urls from cross product of nouns/verbs...itertools.product?
urlpatterns = patterns("a10_horizon.dashboard.a10networks.a10scaling.views",
                       url(r'^$',
                           views.IndexView.as_view(),
                           name='index'),
                       url(r'^scalingpolicy/add$',
                           views.AddPolicyView.as_view(),
                           name='addscalingpolicy'),
                       url(r'^scalingpolicy/update/(?P<scaling_policy_id>[^/]*)$',
                           views.UpdatePolicyView.as_view(),
                           name='updatescalingpolicy'),
                       url(r'^scalingaction/add/$',
                           views.AddActionView.as_view(),
                           name='addaction'),
                       url(r'^action/update/(?P<id>[^/]*)$',
                           views.UpdateActionView.as_view(),
                           name='updateaction'),
                       url(r'^alarm/add/$',
                           views.AddAlarmView.as_view(),
                           name='addalarm'),
                       url(r'^alarm/update/(?P<id>[^/]*)$',
                           views.UpdateAlarmView.as_view(),
                           name='updatealarm'),
                       url(r'^scalingpolicy/(?P<scaling_policy_id>[^/]*)/addreaction$',
                           views.AddReactionView.as_view(),
                           name='addreaction'),
                       url(r'^scalingpolicy/(?P<scaling_policy_id>[^/]*)/detail$',
                           views.PolicyDetailView.as_view(),
                           name='scalingpolicydetail'),
                       url(r'^scalinggroup/(?P<scaling_group_id>[^/]*)/detail$',
                           views.GroupDetailView.as_view(),
                           name='scalinggroupdetail'))
