#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'netcharm'

#from django.contrib import admin
from django.db import models

from django.core.exceptions import ValidationError

from django.utils.translation import ugettext as _

from datetime import date

class Config(models.Model):
    name = models.CharField(_('Name'), max_length=32)
    value = models.CharField(_('Value'), max_length=256)

    def __unicode__(self):
        return self.name

    class Admin:
        pass


class BookEditValidator():

    @staticmethod
    def DigitValidator(value):
        if not value.isdigit():
            raise ValidationError(_(u'%s not a digit') % value)
        pass

    @staticmethod
    def isbn10(value):
        if not value.isdigit():
            raise ValidationError(_(u'%s not a digit') % value)
        if len(value) != 10:
            raise ValidationError(_(u'%s length less 10') % value)
            #if re.match(r’[+-]?\d+$’, ‘-1234′):
        pass

    @staticmethod
    def isbn13(value):
        if not value.isdigit():
            raise ValidationError(_(u'%s not a digit') % value)
        if len(value) != 13:
            raise ValidationError(_(u'%s length less 13') % value)
        pass
    name = models.CharField(_('Media'), max_length=32)

    def __unicode__(self):
        return self.name

    class Admin:
        pass


class Category(models.Model):
    name = models.CharField(_('Category'), max_length=32)

    def __unicode__(self):
        return self.name

    class Admin:
        pass


class Location(models.Model):
    name = models.CharField(_('Location'), max_length=32)

    def __unicode__(self):
        return self.name

    class Admin:
        pass


class State(models.Model):
    name = models.CharField(_('Location'), max_length=32)

    def __unicode__(self):
        return self.name

    class Admin:
        pass


class Media(models.Model):
    name = models.CharField(_('Media'), max_length=32)

    def __unicode__(self):
        return self.name

    class Admin:
        pass


class Statistic(models.Model):
    STYLE_CHOICES = (
        ( u'histogram', _('Histogram') ),
        ( u'line', _('Line') ),
        ( u'pie', _('Pie') ),
    )

    FIELD_CHOICES = (
        ( u'pubdate', _('Date Published') ),
        ( u'boughtdate', _('Date Bought') ),
        ( u'state', _('State') ),
        ( u'read_tags', _('Reading Tags') ),
        ( u'rating', _('Rating') ),
        ( u'category', _('Category') ),
        ( u'location', _('Location') ),
        ( u'media', _('Media') ),
        ( u'publisher', _('Publisher') ),
        ( u'binding', _('Binding') ),
        ( u'author', _('Author') ),
        ( u'translator', _('Translator') ),
    )

    CONDITION_CHOICES = (
        ( u'>' , _('>') ),
        ( u'>=', _('>=') ),
        ( u'=' , _('=') ),
        ( u'<=', _('<=') ),
        ( u'<' , _('<') ),
        ( u'*=' , _('*=') ),
    )

    name = models.CharField(_('Name'), max_length=32)
    style = models.CharField(_('Style'), max_length=32, choices=STYLE_CHOICES)
    # field = models.CharField(_('Field'), max_length=32, choices=FIELD_CHOICES)
    # condition = models.CharField(_('condition'), max_length=4, choices=CONDITION_CHOICES)
    # value = models.CharField(_('Value'), max_length=256)
    setting = models.CharField(_('Value'), max_length=256)
    template = models.CharField(_('Template'), max_length=256)

    def __unicode__(self):
        return self.name

    class Admin:
        pass


class Book(models.Model):
    today_str = format(u"(%s %s)" % (_("etc."), date.today().isoformat()))

    isbn10       = models.CharField(_('ISBN10'), default='', max_length=10, blank=True)#, validators=[BookEditValidator.isbn10])
    isbn13       = models.CharField(_('ISBN13'), max_length=13, validators=[BookEditValidator.isbn13])
    face_l       = models.URLField(_('Face_L'), default='', max_length=256, blank=True)
    face_m       = models.URLField(_('Face_M'), default='', max_length=256, blank=True)
    face_s       = models.URLField(_('Face_S'), default='', max_length=256, blank=True)
    title        = models.CharField(_('Title'), max_length=128)
    subtitle     = models.CharField(_('Subtitle'), default='', max_length=128, blank=True)
    pages        = models.SmallIntegerField(_('Pages'), default=0, blank=True, null=True)
    author       = models.CharField(_('Author'), default='', max_length=256, blank=True)
    translator   = models.CharField(_('Translator'), default='', max_length=256, blank=True)
    publisher    = models.CharField(_('Publisher'), default='', max_length=256, blank=True)
    price        = models.DecimalField(_('Price'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
    boughtprice  = models.DecimalField(_('Price Bought'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
    binding      = models.CharField(_('Binding'), default='', max_length=128, blank=True)
    pubdate      = models.DateField(_('Date Published'), blank=True, null=True, help_text=today_str)
    boughtdate   = models.DateField(_('Date Bought'), blank=True,  null=True, help_text=today_str)
    author_intro = models.TextField(_('Author Intro'), default='', blank=True)
    summary      = models.TextField(_('Summary'), default='', blank=True)
    tags         = models.TextField(_('Tags'), default='', blank=True)
    rating       = models.DecimalField(_('Rating'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
    read_pages   = models.SmallIntegerField(_('Read Pages'), default=0, blank=True,  null=True, help_text=format(u"(%s)" % (_("Pages Be Read"))))
    read_start   = models.DateField(_('Reading Start'), blank=True,  null=True, help_text=today_str)
    read_end     = models.DateField(_('Reading Finished'), blank=True,  null=True, help_text=today_str)
    read_tags    = models.TextField(_('Reading Tags'), default='', blank=True)
    memo         = models.TextField(_('Memo'), default='', blank=True)
    state        = models.ForeignKey(State   , default=0, blank=True, null=True, verbose_name=_('State'))
    category     = models.ForeignKey(Category, default=0, blank=True, null=True, verbose_name=_('Category'))
    location     = models.ForeignKey(Location, default=0, blank=True, null=True, verbose_name=_('Location'))
    media        = models.ForeignKey(Media, default=0, blank=True, null=True, verbose_name=_('Media'))

    def __unicode__(self):
        return self.isbn13

    class Admin:
        pass


# class Music(models.Model):
#     today_str = format(u"(%s %s)" % (_("etc."), date.today().isoformat()))
#
#     isbn10       = models.CharField(_('ISBN10'), default='', max_length=10, blank=True, validators=[BookEditValidator.isbn10])
#     isbn13       = models.CharField(_('ISBN13'), max_length=13, validators=[BookEditValidator.isbn13])
#     face_l       = models.URLField(_('Face_L'), default='', max_length=256, blank=True)
#     face_m       = models.URLField(_('Face_M'), default='', max_length=256, blank=True)
#     face_s       = models.URLField(_('Face_S'), default='', max_length=256, blank=True)
#     title        = models.CharField(_('Title'), max_length=128)
#     subtitle     = models.CharField(_('Subtitle'), default='', max_length=128, blank=True)
#     author       = models.CharField(_('Author'), default='', max_length=256, blank=True)
#     translator   = models.CharField(_('Translator'), default='', max_length=256, blank=True)
#     publisher    = models.CharField(_('Publisher'), default='', max_length=256, blank=True)
#     price        = models.DecimalField(_('Price'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
#     boughtprice  = models.DecimalField(_('Price Bought'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
#     binding      = models.CharField(_('Binding'), default='', max_length=128, blank=True)
#     pubdate      = models.DateField(_('Date Published'), blank=True, null=True, help_text=today_str)
#     boughtdate   = models.DateField(_('Date Bought'), blank=True,  null=True, help_text=today_str)
#     author_intro = models.TextField(_('Author Intro'), default='', blank=True)
#     summary      = models.TextField(_('Summary'), default='', blank=True)
#     tags         = models.TextField(_('Tags'), default='', blank=True)
#     rating       = models.DecimalField(_('Rating'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
#     read_pages   = models.SmallIntegerField(_('Read Pages'), default=0, blank=True,  null=True, help_text=format(u"(%s)" % (_("Pages Be Read"))))
#     read_start   = models.DateField(_('Reading Start'), blank=True,  null=True, help_text=today_str)
#     read_end     = models.DateField(_('Reading Finished'), blank=True,  null=True, help_text=today_str)
#     state        = models.ForeignKey(State   , default=0, blank=True, null=True, verbose_name=_('State'))
#     category     = models.ForeignKey(Category, default=0, blank=True, null=True, verbose_name=_('Category'))
#     location     = models.ForeignKey(Location, default=0, blank=True, null=True, verbose_name=_('Location'))
#     media        = models.ForeignKey(Media   , default=0, blank=True, null=True, verbose_name=_('Media'))
#
#     def __unicode__(self):
#         return self.title
#
#     class Admin:
#         pass
#
# class Movie(models.Model):
#     today_str = format(u"(%s %s)" % (_("etc."), date.today().isoformat()))
#
#     isbn10       = models.CharField(_('ISBN10'), default='', max_length=10, blank=True, validators=[BookEditValidator.isbn10])
#     isbn13       = models.CharField(_('ISBN13'), max_length=13, validators=[BookEditValidator.isbn13])
#     face_l       = models.URLField(_('Face_L'), default='', max_length=256, blank=True)
#     face_m       = models.URLField(_('Face_M'), default='', max_length=256, blank=True)
#     face_s       = models.URLField(_('Face_S'), default='', max_length=256, blank=True)
#     title        = models.CharField(_('Title'), max_length=128)
#     subtitle     = models.CharField(_('Subtitle'), default='', max_length=128, blank=True)
#     author       = models.CharField(_('Author'), default='', max_length=256, blank=True)
#     translator   = models.CharField(_('Translator'), default='', max_length=256, blank=True)
#     publisher    = models.CharField(_('Publisher'), default='', max_length=256, blank=True)
#     price        = models.DecimalField(_('Price'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
#     boughtprice  = models.DecimalField(_('Price Bought'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
#     binding      = models.CharField(_('Binding'), default='', max_length=128, blank=True)
#     pubdate      = models.DateField(_('Date Published'), blank=True, null=True, help_text=today_str)
#     boughtdate   = models.DateField(_('Date Bought'), blank=True,  null=True, help_text=today_str)
#     author_intro = models.TextField(_('Author Intro'), default='', blank=True)
#     summary      = models.TextField(_('Summary'), default='', blank=True)
#     tags         = models.TextField(_('Tags'), default='', blank=True)
#     rating       = models.DecimalField(_('Rating'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
#     read_pages   = models.SmallIntegerField(_('Read Pages'), default=0, blank=True,  null=True, help_text=format(u"(%s)" % (_("Pages Be Read"))))
#     read_start   = models.DateField(_('Reading Start'), blank=True,  null=True, help_text=today_str)
#     read_end     = models.DateField(_('Reading Finished'), blank=True,  null=True, help_text=today_str)
#     state        = models.ForeignKey(State   , default=0, blank=True, null=True, verbose_name=_('State'))
#     category     = models.ForeignKey(Category, default=0, blank=True, null=True, verbose_name=_('Category'))
#     location     = models.ForeignKey(Location, default=0, blank=True, null=True, verbose_name=_('Location'))
#     media        = models.ForeignKey(Media   , default=0, blank=True, null=True, verbose_name=_('Media'))
#
#     def __unicode__(self):
#         return self.title
#
#     class Admin:
#         pass
#


# admin.site.register(Statistic)
# admin.site.register(Config)
# admin.site.register(Media)
# admin.site.register(State)
# admin.site.register(Category)
# admin.site.register(Location)
# admin.site.register(Book)

# admin.site.register(Music)
# admin.site.register(Movie)
