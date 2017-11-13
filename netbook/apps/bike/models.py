# -*- coding: utf-8 -*-

__author__ = 'netcharm'

#######################

# from django.db import models

# Create your models here.

from django.db import models

from django.utils.translation import ugettext as _

from datetime import date


class Config(models.Model):
    name = models.CharField(_('Name'), max_length=32)
    value = models.CharField(_('Value'), max_length=256)

    def __unicode__(self):
        return self.name


class User(models.Model):
    name = models.CharField(_('Name'), max_length=32)
    password = models.CharField(_('Password'), max_length=32, blank=True)

    def __unicode__(self):
        return self.name



class Bike(models.Model):
    today_str = format(u"(%s %s)" % (_("etc."), date.today().isoformat()))

    name = models.CharField(_('Name'), max_length=64)
    brand = models.CharField(_('Brand'), max_length=64, default='', blank=True)
    model = models.CharField(_('Model'), max_length=64, default='', blank=True)
    factory = models.CharField(_('Factory'), max_length=128, default='', blank=True)
    year = models.DateField(_('Year'), null=True, help_text=today_str, blank=True)
    description = models.TextField(_('Description'), default='', blank=True)
    memo = models.TextField(_('Memo'), default='', blank=True)

    def __unicode__(self):
        return self.name



class TrackLog(models.Model):
    name = models.CharField(_('Name'), max_length=128)
    speed_avg = models.DecimalField(_('Speed Avg.'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
    speed_min = models.DecimalField(_('Speed Min.'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
    speed_max = models.DecimalField(_('Speed Max.'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
    speed_avg = models.DecimalField(_('Price Bought'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)


    #logfile = models.FileField(_('Log File'), upload_to='', blank=True,  null=True)


    def __unicode__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(_('Category'), max_length=32)

    def __unicode__(self):
        return self.name

