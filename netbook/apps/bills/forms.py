# -*- coding: utf-8 -*-

__author__ = 'netcharm'

from django import forms
#from django.contrib.admin import widgets

from models import Config, Bill, FixedAsset

class ConfigEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = Config

    def __init__(self, *args, **kwargs):
        super(ConfigEditForm, self).__init__(*args, **kwargs)

        self.fields['value'].widget.attrs['size']  = 128

    pass



class FixedAssetEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = FixedAsset

    def __init__(self, *args, **kwargs):
        super(FixedAssetEditForm, self).__init__(*args, **kwargs)

        for field in  self.fields:
            if   field == 'description':
                self.fields[field].widget.attrs['size'] = 96
            elif field == 'property_bank':
                self.fields[field].widget.attrs['size'] = 96
            elif field == 'property_user':
                self.fields[field].widget.attrs['size'] = 96
            # elif field == 'property_account':
            else:
                self.fields[field].widget.attrs['size'] = 32
    pass


class BillEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = Bill

    def __init__(self, *args, **kwargs):
        super(BillEditForm, self).__init__(*args, **kwargs)

        for field in  self.fields:
            if not self.fields[field].required:
                #self.fields[field].hidden_widget = forms.HiddenInput()
                if field == 'location'                    : continue

                if field == 'bill_date'                   : continue

                if field == 'private_electricity_last'    : continue
                if field == 'private_electricity_current' : continue
                if field == 'private_electricity_bill'    : continue

                if field == 'private_water_last'          : continue
                if field == 'private_water_current'       : continue
                if field == 'private_water_bill'          : continue

                if field == 'public_electricity'          : continue
                if field == 'public_water'                : continue
                if field == 'public_electricity_elevator' : continue
                if field == 'public_water_relay'          : continue

                if field == 'property_cost'               : continue
                if field == 'property_balance_last'       : continue
                if field == 'property_balance_current'    : continue

                self.fields[field].widget = forms.HiddenInput()
                pass

        pass

    pass

