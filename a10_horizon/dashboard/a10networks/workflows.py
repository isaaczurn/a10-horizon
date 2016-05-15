# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.

import logging

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import workflows

# a10_horizon.dashboard.api.client.Client extends neutron.api.client.Client
from a10_horizon.dashboard.api import certificates as api
from openstack_dashboard.api import lbaas as lbaas_api

# TODO(Pull these from A10 constants)
AVAILABLE_PROTOCOLS = ('HTTP', 'HTTPS', 'TCP')
AVAILABLE_METHODS = ('ROUND_ROBIN', 'LEAST_CONNECTIONS', 'SOURCE_IP')

LOG = logging.getLogger(__name__)

