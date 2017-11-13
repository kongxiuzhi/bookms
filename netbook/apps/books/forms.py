#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

__author__ = 'netcharm'

from django import forms
#from django.contrib.admin import widgets

from models import Config, Book, Category, Location, State, Media, Statistic

class ConfigEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = Config

    def __init__(self, *args, **kwargs):
        super(ConfigEditForm, self).__init__(*args, **kwargs)

        self.fields['value'].widget.attrs['size']  = 128


class CategoryEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = Category


class LocationEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = Location


class StateEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = State


class MediaEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = Media


class StatisticEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = Statistic

    def __init__(self, *args, **kwargs):
        super(StatisticEditForm, self).__init__(*args, **kwargs)

        self.fields['setting'].widget.attrs['size']  = 128
        self.fields['template'].widget.attrs['size'] = 128


class BookEditForm(forms.ModelForm):
    required_css_class = 'ui-state-highlight'
    error_css_class = 'ui-state-error'

    class Meta:
        model = Book

    def __init__(self, *args, **kwargs):
        super(BookEditForm, self).__init__(*args, **kwargs)

        for field in  self.fields:
            if not self.fields[field].required:
                #self.fields[field].hidden_widget = forms.HiddenInput()
                if field == 'category'     : continue
                if field == 'location'     : continue
                if field == 'media'        : continue
                if field == 'state'        : continue
                if field == 'summary'      : continue
                if field == 'pubdate'      : continue
                if field == 'boughtdate'   : continue
                if field == 'price'        : continue
                if field == 'boughtprice'  : continue
                if field == 'rating'       : continue
                if field == 'subtitle'     : continue
                if field == 'author'       : continue
                if field == 'author_intro' : continue
                if field == 'translator'   : continue
                if field == 'tags'         : continue
                if field == 'read_pages'   : continue
                if field == 'read_start'   : continue
                if field == 'read_end'     : continue
                if field == 'read_tags'    : continue
                if field == 'publisher'    : continue
                if field == 'pages'        : continue
                if field == 'isbn10'       : continue
                if field == 'binding'      : continue
                if field == 'memo'         : continue


                self.fields[field].widget = forms.HiddenInput()
                pass

        #self.fields['category'].widget = forms.ModelChoiceField(Category)
        #self.fields['location'].widget = forms.ModelChoiceField(Location)
        self.fields['title'].widget.attrs['size']    = 96
        self.fields['subtitle'].widget.attrs['size'] = 96
        self.fields['author'].widget.attrs['size']   = 96
        self.fields['author_intro'].widget.attrs['style'] = 'height:64px'
        self.fields['tags'].widget.attrs['style'] = 'height:64px'
        self.fields['read_tags'].widget.attrs['style'] = 'height:64px'

        self.fields['category'].widget.attrs['style'] = 'width:140px'
        self.fields['location'].widget.attrs['style'] = 'width:140px'
        self.fields['state'].widget.attrs['style'] = 'width:140px'
        self.fields['media'].widget.attrs['style'] = 'width:140px'

        #self.fields['pubdate'].widget = widgets.AdminDateWidget()
        #self.fields['boughtdate'].widget = widgets.AdminDateWidget()

        pass

    pass

