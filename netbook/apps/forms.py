# -*- coding: utf-8 -*-

__author__ = 'netcharm'

from django import forms
#from django.contrib.admin import widgets

from models import Config, App

class ConfigEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = Config

    def __init__(self, *args, **kwargs):
        super(ConfigEditForm, self).__init__(*args, **kwargs)

        self.fields['value'].widget.attrs['size']  = 128

    pass


class AppEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = App

    def __init__(self, *args, **kwargs):
        super(AppEditForm, self).__init__(*args, **kwargs)

    pass
