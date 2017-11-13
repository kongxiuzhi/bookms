#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

__author__ = 'netcharm'

from django.db import models

#from django.core.exceptions import ValidationError

from django.utils.translation import ugettext as _

from datetime import date

class Config(models.Model):
    key = models.CharField(_('Key'), max_length=32)
    value = models.CharField(_('Value'), max_length=256)

    def __unicode__(self):
        return self.key


class FixedAsset(models.Model):
    today_str = format(u"(%s %s)" % (_("etc."), date.today().isoformat()))

    description            = models.CharField(_('Description'), max_length=256)
    realestate_certificate = models.CharField(_('Real Estate Number'), max_length=64, blank=True,  null=True)
    landuse_certificate    = models.CharField(_('Land Use Number'), max_length=64, blank=True,  null=True)

    owner                  = models.CharField(_('Owner'), max_length=128, blank=True,  null=True)
    id_number              = models.CharField(_('ID Number'), max_length=64, blank=True,  null=True)
    bought_date            = models.DateField(_('Bought Date'), blank=True, null=True, help_text=today_str)
    bought_price           = models.DecimalField(_('Bought Price'), default=0, max_digits=12, decimal_places=2, blank=True,  null=True)
    value                  = models.DecimalField(_('Value'), default=0, max_digits=12, decimal_places=2, blank=True,  null=True)
    country                = models.CharField(_('Country'), max_length=128, blank=True,  null=True)
    province               = models.CharField(_('Province'), max_length=128, blank=True,  null=True)
    city                   = models.CharField(_('City'), max_length=128, blank=True,  null=True)
    address                = models.TextField(_('Address'), max_length=256, blank=True,  null=True)
    latitude               = models.DecimalField(_('Latitude'), default=0, max_digits=8, decimal_places=5, blank=True,  null=True)
    longitude              = models.DecimalField(_('Longitude'), default=0, max_digits=8, decimal_places=5, blank=True,  null=True)
    altitude               = models.DecimalField(_('Altitude'), default=0, max_digits=8, decimal_places=5, blank=True,  null=True)
    acreage                = models.DecimalField(_('Acreage'), default=0, max_digits=8, decimal_places=2, blank=True,  null=True)
    tele                   = models.CharField(_('Telephone'), max_length=32, blank=True,  null=True)
    email                  = models.EmailField(_('E-Mail'), max_length=128, blank=True,  null=True)
    postal                 = models.CharField(_('Postal'), max_length=32, blank=True,  null=True)
    note                   = models.TextField(_('Note'), max_length=32, blank=True,  null=True)

    property_bank          = models.CharField(_('Property Bank'), max_length=128, blank=True,  null=True)
    property_user          = models.CharField(_('Property Name'), max_length=128, blank=True,  null=True)
    property_account       = models.CharField(_('Property Account'), max_length=64, blank=True,  null=True)
    property_tele          = models.CharField(_('Property Telephone'), max_length=32, blank=True,  null=True)
    property_email         = models.CharField(_('Property EMail'), max_length=32, blank=True,  null=True)
    property_contact       = models.CharField(_('Property Contact'), max_length=32, blank=True,  null=True)

    property_unitprice     = models.DecimalField(_('Property Unit Price'), default=1, max_digits=8, decimal_places=2, blank=True,  null=True)

    fulladdress            = ''
    property_cost          = 0

    def calc(self):
        self.fulladdress = '%s%s%s%s' % (self.country, self.province, self.city, self.address)
        if self.property_unitprice and self.acreage:
            self.property_cost = self.property_unitprice * self.acreage

        pass

    def __unicode__(self):
        self.calc()
        return self.description


class Bill(models.Model):
    today_str = format(u"(%s %s)" % (_("etc."), date.today().isoformat()))
    date_format = [
        '%Y-%m',
        '%Y/%m',
        '%y/%m',
        '%m/%Y',
        '%m/%y',
    ]

    #serialnumber = models.CharField(_('Serial Number'), max_length=32)
    location = models.ForeignKey(FixedAsset, default=0, blank=True, null=True, verbose_name=_('Asset Location'))

    bill_date = models.DateField(_('Bill Date'), blank=True, null=True, help_text=today_str)

    private_electricity_last    = models.DecimalField(_('Last Month Electricity Count'), default=0, max_digits=8, decimal_places=2, blank=True,  null=True)
    private_electricity_current = models.DecimalField(_('Current Month Electricity Count'), default=0, max_digits=8, decimal_places=2, blank=True,  null=True)
    private_electricity_bill    = models.DecimalField(_('Current Month Electricity Fee'), default=0, max_digits=8, decimal_places=2)

    private_water_last    = models.DecimalField(_('Last Month Water Count'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
    private_water_current = models.DecimalField(_('Current Month Water Count'), default=0, max_digits=5, decimal_places=2, blank=True,  null=True)
    private_water_bill    = models.DecimalField(_('Current Month Water Fee'), default=0, max_digits=5, decimal_places=2)

    public_electricity          = models.DecimalField(_('Public Electricity Fee'), default=0, max_digits=8, decimal_places=2, blank=True,  null=True)
    public_water                = models.DecimalField(_('Public Water Fee'), default=0, max_digits=8, decimal_places=2, blank=True,  null=True)
    public_electricity_elevator = models.DecimalField(_('Public Electricity Elevator Fee'), default=0, max_digits=8, decimal_places=2, blank=True,  null=True)
    public_water_relay          = models.DecimalField(_('Public Water Relay Fee'), default=0, max_digits=8, decimal_places=2, blank=True,  null=True)

    property_cost            = models.DecimalField(_('Property Fee'), default=0, max_digits=8, decimal_places=2)
    property_balance_last    = models.DecimalField(_('Last Property Balance'), default=0, max_digits=8, decimal_places=2, blank=True,  null=True)
    property_balance_current = models.DecimalField(_('Current Property Balance'), default=0, max_digits=8, decimal_places=2, blank=True,  null=True)


    #
    # Calculating the fee
    #
    water_unitprice = 0
    water_count = 0

    electricity_unitprice = 0
    electricity_count = 0

    property_unitprice = 0
    real_property_unitprice = 0

    total_fee_ew = 0
    total_fee_public = 0
    total_fee_all = 0

    def calc(self):
        if self.private_water_current and self.private_water_last:
            self.water_count = self.private_water_current - self.private_water_last
            if (self.private_water_bill >= 0) and (self.water_count > 0):
                self.water_unitprice = self.private_water_bill / self.water_count

        if self.private_electricity_current and self.private_electricity_last:
            self.electricity_count = self.private_electricity_current - self.private_electricity_last
            if (self.private_electricity_bill >= 0) and (self.electricity_count > 0):
                self.electricity_unitprice = self.private_electricity_bill / self.electricity_count

        if  self.property_cost and self.location and self.location.acreage:
            if (self.property_cost >= 0) and (self.location.acreage > 0):
                self.real_property_unitprice = self.property_cost / self.location.acreage

        if self.location and self.location.property_unitprice:
            self.property_unitprice = self.location.property_unitprice


        if self.private_water_bill and (self.private_water_bill >= 0):
            private_water_bill = self.private_water_bill
        else:
            private_water_bill = 0


        if self.private_electricity_bill and (self.private_electricity_bill >= 0):
            private_electricity_bill = self.private_electricity_bill
        else:
            private_electricity_bill = 0

        self.total_fee_ew = private_water_bill + private_electricity_bill


        if self.public_electricity and (self.public_electricity >= 0):
            public_electricity = self.public_electricity
        else:
            public_electricity = 0

        if self.public_electricity_elevator and (self.public_electricity_elevator >= 0):
            public_electricity_elevator = self.public_electricity_elevator
        else:
            public_electricity_elevator = 0

        if self.public_water and (self.public_water >= 0):
            public_water = self.public_water
        else:
            public_water = 0

        if self.public_water_relay and (self.public_water_relay >= 0):
            public_water_relay = self.public_water_relay
        else:
            public_water_relay = 0

        self.total_fee_public = public_electricity + public_electricity_elevator + public_water + public_water_relay


        if self.total_fee_ew:
            total_fee_ew = self.total_fee_ew
        else:
            total_fee_ew = 0

        if self.total_fee_public:
            total_fee_public = self.total_fee_public
        else:
            total_fee_public = 9

        if self.property_cost:
            property_cost = self.property_cost
        else:
            property_cost = 9

        self.total_fee_all = total_fee_ew + total_fee_public + property_cost

        pass

    def __unicode__(self):
        self.calc()
        return self.location

