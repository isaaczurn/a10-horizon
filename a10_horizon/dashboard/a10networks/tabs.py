# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.

import logging

from django.utils.translation import ugettext_lazy as _

from a10_neutron_lbaas import a10_config
from horizon import tabs
from horizon import exceptions

from a10_horizon.dashboard.a10networks import tables
from a10scaling import tabs as scaling_tabs
from a10_horizon.dashboard.api import certificates as cert_api


LOG = LOG = logging.getLogger(__name__)


class AdvancedTab(tabs.TableTab):
    table_classes = (tables.AdvancedTable,)
    name = _("Advanced")
    slug = "advanced"
    template_name = "horizon/common/_detail_table.html"

    def get_advancedtable_data(self):
        cfg = a10_config.A10Config()
        members = []

        if hasattr(cfg, 'devices'):
            for k, v in cfg.devices.items():
                v['name'] = k
                members.append(v)

        return members
