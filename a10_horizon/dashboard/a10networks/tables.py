# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.

import logging
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon import tables

LOG = logging.getLogger(__name__)


def a10_ax_url(device):
    ip = device.get('ip', '')
    host = device.get('host', '')
    port = str(device.get('port', ''))
    port = port and ':' + port
    proto = device.get('protocol', 'https')

    host = ip or host
    if not host:
        return ''

    return "%s://%s%s" % (proto, host, port)


class AdvancedTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"))
    host = tables.Column('host', verbose_name=_("Host"), link=a10_ax_url)

    class Meta(object):
        name = "advancedtable"
        verbose_name = _("Advanced")

    def get_object_id(self, member):
        return member['name']
