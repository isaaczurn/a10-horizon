# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.

import horizon
import logging

from openstack_dashboard.api import neutron as neutron_api

LOG = logging.getLogger(__name__)


class NeutronExtensionPanelBase(horizon.Panel):

    """Name of Neutron extension(s) that enables the panel.
    """

    REQUIRED_EXTENSIONS = []

    def allowed(self, context):
        exts = []

        if len(self.REQUIRED_EXTENSIONS) > 0:
            # Ensure all of the named extensions are present.  Else, return false.
            try:
                exts = [x["alias"] for x in neutron_api.list_extensions(context.request)]
                missing_exts = [x not in exts for x in self.REQUIRED_EXTENSIONS]
                if len(missing_exts) > 0:
                    msg = "The following extensions are required to load this plugin:" + "\n"
                    msg += "\n".join(missing_exts)
                    msg += "\nPlease contact A10 Account Team to enable."
                    LOG.error(msg)
                    return False
                else:
                    return True

            except Exception as ex:
                LOG.error("There was a problem retrieving the extension list.  See exception for details.")
                LOG.exception(ex)

        # If we got this far without returning anything, something is wrong. No display.
        return True
