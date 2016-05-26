# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.utils.translation import ugettext_lazy as _
import logging

import horizon

LOG = logging.getLogger(__name__)


class A10SSLPanel(horizon.Panel):
    name = _("SSL")
    slug = "a10ssl"
    permissions = ("openstack.services.network", )

    # def can_register(self):
    #     rv = False

    #     try:
    #         import a10_openstack  # noqa
    #         rv = True
    #     except Exception:
    #         msg = "{0} cannot be displayed.  Please contact A10 Account Team to enable."
    #         rv = False
    #         LOG.exception(msg.format("A10 SSL"))
    #     return rv
