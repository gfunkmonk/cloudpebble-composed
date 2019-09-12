from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
from django.forms import ModelForm, Select

from ide.models.user import UserSettings


class SettingsForm(ModelForm):
    class Meta(object):
        model = UserSettings
        exclude = ('user', 'accepted_terms', 'whats_new')
        widgets = {
            'use_spaces': Select
        }
