# Copyright (C) 2016, A10 Networks Inc. All rights reserved.

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tabs
from horizon import views
from horizon import workflows
from horizon.utils import memoized

import logging

import re

LOG = logging.getLogger(__name__)


class IndexView(views.HorizonTemplateView):
    pass
