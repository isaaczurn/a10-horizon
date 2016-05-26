# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.

import importlib
import logging
import re

from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)


def post_hack(self, request, *args, **kwargs):
    # These import statements break the pip install when they're global
    from a10_horizon.dashboard.api import certificates as cert_api
    from horizon import exceptions
    from horizon import messages
    from openstack_dashboard import api

    obj_ids = request.POST.getlist('object_ids')
    action = request.POST['action']
    m = re.search('.delete([a-z]+)', action).group(1)
    if obj_ids == []:
        obj_ids.append(re.search('([0-9a-z-]+)$', action).group(1))
    if m == 'monitor':
        for obj_id in obj_ids:
            try:
                api.lbaas.pool_health_monitor_delete(request, obj_id)
                messages.success(request, _('Deleted monitor %s') % obj_id)
            except Exception as e:
                exceptions.handle(request,
                                  _('Unable to delete monitor. %s') % e)
    if m == 'pool':
        for obj_id in obj_ids:
            try:
                api.lbaas.pool_delete(request, obj_id)
                messages.success(request, _('Deleted pool %s') % obj_id)
            except Exception as e:
                exceptions.handle(request,
                                  _('Unable to delete pool. %s') % e)
    if m == 'member':
        for obj_id in obj_ids:
            try:
                api.lbaas.member_delete(request, obj_id)
                messages.success(request, _('Deleted member %s') % obj_id)
            except Exception as e:
                exceptions.handle(request,
                                  _('Unable to delete member. %s') % e)
    if m == 'vip':
        for obj_id in obj_ids:
            try:
                vip_id = api.lbaas.pool_get(request, obj_id).vip_id
            except Exception as e:
                exceptions.handle(request,
                                  _('Unable to locate VIP to delete. %s')
                                  % e)
            if vip_id is not None:
                try:
                    api.lbaas.vip_delete(request, vip_id)
                    messages.success(request, _('Deleted VIP %s') % vip_id)
                except Exception as e:
                    exceptions.handle(request,
                                      _('Unable to delete VIP. %s') % e)

    if m == 'certificate':
        for obj_id in obj_ids:
            try:
                cert_api.certificate_delete(request, obj_id)
                messages.success(request, _("Deleted certificate. %s") % obj_id)
            except Exception as e:
                exceptions.handle(request, _('Unable to delete Certificate. %s') % e)

    if m == 'certificatebinding':
        for obj_id in obj_ids:
            try:
                cert_api.certificate_binding_delete(request, obj_id)
                messages.success(request, _("Deleted certificate association. %s") % obj_id)
            except Exception as e:
                exceptions.handle(request, _("Unable to delete certificate association %s") %
                                  obj_id)

    return self.get(request, *args, **kwargs)


def add_tab(url, tab, idx=None):
    logger.debug("add_tab(), url:%s, tabl: %s, idx: %s", url, tab, idx)
    # Get the index view via it's url name
    view_func = resolve(reverse(url)).func
    module = importlib.import_module(view_func.__module__)
    view = getattr(module, view_func.__name__)

    # Import the view and if it has a tab_group_class
    # we'll add to it.
    if hasattr(view, 'tab_group_class'):
        tab_list = list(view.tab_group_class.tabs)
        if tab not in tab_list:
            if idx is None:
                idx = len(tab_list)

            tab_list.insert(idx, tab)
            view.tab_group_class.tabs = tuple(tab_list)
