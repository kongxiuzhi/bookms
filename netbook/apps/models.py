# -*- coding: utf-8 -*-

__author__ = 'netcharm'

#from django.contrib import admin
from django.db import models

#from django.core.exceptions import ValidationError

from django.utils.translation import ugettext as _

from datetime import date

class Config(models.Model):
    key = models.CharField(_('Key'), max_length=32)
    value = models.CharField(_('Value'), max_length=256)

    def __unicode__(self):
        return self.key

    class Admin:
        pass

class App(models.Model):
    name        = models.CharField(_('App Name'), max_length=32)
    description = models.CharField(_('Description'), max_length=256, blank=True,  null=True)
    # url         = models.URLField(_('URL'))
    # icon        = models.URLField(_('Icon'), blank=True,  null=True)
    url         = models.CharField(_('URL'), max_length=256 )
    icon        = models.CharField(_('Icon'), max_length=256, blank=True,  null=True)
    order       = models.IntegerField(_('Order'), max_length=16, blank=True,  null=True)

    def __unicode__(self):
        return self.description

    class Admin:
        pass

