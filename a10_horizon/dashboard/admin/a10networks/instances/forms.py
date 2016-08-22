from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

import helper

def array_to_choices(choices=[]):
    return map(lambda x: (x, x), choices)


class MigrateDevice(forms.SelfHandlingForm):
    instance_id = forms.CharField(label=_("Instance ID"),
                                  widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                                              required=True)
    host = forms.ChoiceField(label=_("Host IP"),
                              required=True)

    def __init__(self, *args, **kwargs):
        super(MigrateDevice, self).__init__(*args, **kwargs)
        instance_id = str(kwargs.get("initial").get("nova_instance_id"))
        self.fields["host"].choices = array_to_choices(helper.get_hosts(self.request))
        self.fields["instance_id"].initial = instance_id

    def handle(self, request, context):
        host_id = context["id"]
        try:
            migrate = helper.migrate(request,
                    context['instance_id'],
                    context['host'])
            return migrate
        except Exception:
            exceptions.handle(request,
                    _('Unable to make the migration.'))


