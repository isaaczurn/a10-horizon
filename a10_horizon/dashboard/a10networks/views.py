# Copyright (C) 2014-2015, A10 Networks Inc. All rights reserved.

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from horizon import messages
from horizon import tabs
from horizon import workflows
from horizon import views
import logging

from a10_horizon.dashboard.api import certificates as cert_api
from a10_horizon.dashboard.api import scaling as scaling_api
from a10_horizon.dashboard.a10networks import forms as project_forms
from a10_horizon.dashboard.a10networks import workflows as project_workflows
from a10_horizon.dashboard.a10networks import tabs as project_tabs

import re

LOG = logging.getLogger(__name__)


class IndexView(views.HorizonTemplateView):
    # tab_group_class = "asdf"
    template_name = 'index.html'
