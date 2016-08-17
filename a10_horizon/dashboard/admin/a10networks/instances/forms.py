from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

import helper

def array_to_choices(choices=[]):
    return map(lambda x: (x, x), choices)

class MigrateDevice(forms.SelfHandlingForm):
    instance_id = forms.CharField(label=_("Instance ID"),
            widget=forms.HiddenInput(),
            required=true)

    host_list = helper.get_hosts(self.request)

    host = forms.ChoiceField(max_length=255,
            label=_("Host IP"),
            choices=array_to_choices(host_list),
            required=true)


    def handle(self, request, data):
        try:
            migrate = helper.migrate(request,
                    data['instance_id'],
                    data['host'])
            return migrate
        except Exception:
            exceptions.handle(request,
                    _('Unable to make the migration.'))


            def get_hosts(request):
                nova_api.host_list(request)
