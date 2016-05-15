# Copyright (C) 2016, A10 Networks Inc. All rights reserved.

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from horizon import messages
from horizon import tabs
from horizon import views
from horizon import workflows

import logging


import re

LOG = logging.getLogger(__name__)


ACTION = "action"
NOUN = "noun"
PLURAL = "plural"


class IndexView(views.HorizonTemplateView):
    pass
