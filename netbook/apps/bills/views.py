#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

__author__ = 'netcharm'

# Create your views here.

import os
from datetime import date

import json
from xml.dom.minidom import parse, parseString


from django.db.models.signals import post_syncdb, pre_save
from django.dispatch import receiver

from django.utils.translation import ugettext as _

from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404 #, get_list_or_404
from django.shortcuts import render
from django.http import HttpResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.core.servers.basehttp import FileWrapper
from django.core import serializers

from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models import Count

from models import Config, Bill, FixedAsset
from forms import ConfigEditForm, BillEditForm, FixedAssetEditForm

import utils

import models as myapp
# post_syncdb.connect(index, sender=bills_app)

@receiver(pre_save, sender=myapp)
def install(sender, **kwargs):
    pass
    # if kwargs['app'].__name__ == settings.INSTALLED_APPS[-1] + ".models":
    #     pass
        # load fixtures here

#post_syncdb.connect(install)


def index(request):
    return bills.list(request, limit=20, order='-bill_date')


class uri_info:
    app_root = '/bills'
    app_name = _('My Bills')

    location_list = None

    bill_year_list = None
    bill_month_list = None
    buydate_list = None

    tags_list = None

    path = None
    query = None
    filter_key = None
    filter_value = None
    order_key = None

    config = None
    formAddBill = None

    theme = None
    pageitems = 3


#
# Configs
#
class configs:

    @staticmethod
    def set(request):
        key   = request.GET.get('key', '').strip()
        value = request.GET.get('value', '').strip()

        if key and value:
            try:
                cfg = Config.objects.get(key=key)
                cfg.value = value
                cfg.save()
            except ObjectDoesNotExist:
                cfg = Config.objects.create(key=key, value=value)
                cfg.save()

        return HttpResponseRedirect('/bills/config/')

    @staticmethod
    def get(request, key=''):
        key = request.GET.get('key', key).strip()
        value = None
        if key:
            try:
                cfg = Config.objects.get(key=key)
                value = cfg.value
            except:
                pass
        else:
            pass

        return value

    @staticmethod
    def list(request, limit=0):
        qdata = bills.get_nav_list(request)

        latest_config_list = Config.objects.order_by('key')
        context = {
            'config_list': latest_config_list,
            }

        context = bills.make_context(qdata, context)
        return render(request, 'default/bills_config_list.html', context)

    @staticmethod
    def add(request):
        qdata = bills.get_nav_list(request)
        if request.method == 'POST':
            form = ConfigEditForm(request.POST)
            if form.is_valid():
                item_key = form.cleaned_data['key']
                item_value = form.cleaned_data['value']
                try:
                    config = Config.objects.get(key=item_key)
                except ObjectDoesNotExist:
                    config = Config.objects.create(key=item_key)
                config.key = item_key
                config.value = item_value
                config.save()
                return HttpResponseRedirect('/bills/config/')
            else:
                context ={'form': form, }
        else:
            default_values = {
                'key'     : _('Unknown'),
                }
            form = ConfigEditForm(initial=default_values)
            context = {'form': form, }

        context = bills.make_context(qdata, context)
        return render(request, 'default/bills_config_edit.html', context)

    @staticmethod
    def edit(request, config_id):
        qdata = bills.get_nav_list(request)
        config = get_object_or_404(Config, key=config_id)
        if request.method == 'POST':
            form = ConfigEditForm(instance=config, data=request.POST)
            if form.is_valid():
                item_key = form.cleaned_data['key']
                item_value = form.cleaned_data['value']
                try:
                    # config = Config.objects.get(key=item_key)
                    config.key = item_key
                    config.value = item_value
                    config.save()
                except ObjectDoesNotExist:
                    form.save()

                return HttpResponseRedirect('/bills/config/')
            else:
                context = {'form': form,}
        else:
            form = ConfigEditForm(instance=config)
            context = {'form': form, 'config': config, }

        context = bills.make_context(qdata, context)
        return render(request, 'default/media_edit.html', context)

    @staticmethod
    def remove(request, config_id):
        config = get_object_or_404(Config, key=config_id)
        config.delete()
        return HttpResponseRedirect('/bills/config/')


#
# Bills Actions
#
class bills:

    @staticmethod
    def get_nav_list(request):
        """

        :param request:
        :return:
        """
        q = uri_info()

        #import time
        #st = time.clock();

        default_values = {
            'bill_date'         : format(u"%s" % (date.today().isoformat())),
            }
        q.formAddBill = BillEditForm(initial=default_values) # A form bound to the POST data


        # q.location_list = FixedAsset.objects.order_by('description')
        q.location_list = FixedAsset.objects.order_by('city')

        #print('Fetched datas : % 8.4fs' % (time.clock() - st))

        q.bill_year_list = []
        year_list = Bill.objects.all().dates('bill_date', 'year')
        for years in year_list:
            q.bill_year_list.append(years.year)
        q.bill_year_list.sort()

        q.bill_month_list = []
        month_list = Bill.objects.all().dates('bill_date', 'month')
        for months in month_list:
            if not months.month in q.bill_month_list:
                q.bill_month_list.append(months.month)
        q.bill_month_list.sort()

        q.path = request.path
        q.query = request.GET.get('q', '').strip()
        q.filter_key = request.GET.get('f', '').strip()
        q.filter_value = request.GET.get('v', '').strip()
        q.order_key = request.GET.get('o', '').strip()

        q.theme = configs.get(request, 'theme')

        q.pageitems = configs.get(request, 'pageitems')
        q.pageitems =  q.pageitems if q.pageitems else 3


        return  q

    @staticmethod
    def make_context(qdata, context):
        """

        :param qdata:
        :param context:
        :return:
        """
        new_context = dict()
        for item in context:
            new_context[item] = context[item]

        new_context['app_root'] = qdata.app_root
        new_context['app_name'] = _(qdata.app_name)

        new_context['form_add'] = qdata.formAddBill

        new_context['location_list'] = qdata.location_list
        new_context['bill_year_list']  = qdata.bill_year_list
        new_context['bill_month_list']  = qdata.bill_month_list

        new_context['path']           = qdata.path
        new_context['query']          = qdata.query
        new_context['qkey']           = qdata.filter_key
        new_context['qvalue']         = qdata.filter_value
        new_context['order']          = qdata.order_key
        new_context['theme']         = qdata.theme

        return new_context
        pass

    @staticmethod
    def search(request):
        qdata = bills.get_nav_list(request)
        order_key = '-bill_date'
        if qdata.order_key:
            order_key = qdata.order_key

        if qdata.filter_key and qdata.filter_value:
            qf = Q()
            if   qdata.filter_key == 'bill_year':
                qf = Q(bill_date__year=qdata.filter_value)
            elif qdata.filter_key == 'bill_month':
                qf = Q(bill_date__month=qdata.filter_value)
            elif qdata.filter_key == 'location':
                # qf = Q(location__description__contains=qdata.filter_value)
                qf = Q(location__city__contains=qdata.filter_value)

            if qdata.query:
                qset = qf & (
                    Q(location__description__icontains=qdata.query) |
                    Q(location__country__icontains=qdata.query) |
                    Q(location__province__icontains=qdata.query) |
                    Q(location__city__icontains=qdata.query)
                )
            else:
                qset = qf

            results = Bill.objects.filter(qset).order_by(order_key, '-bill_date').distinct()
        elif qdata.query:
            if qdata.query:
                qset = (
                    Q(location__description__icontains=qdata.query) |
                    Q(location__country__icontains=qdata.query) |
                    Q(location__province__icontains=qdata.query) |
                    Q(location__city__icontains=qdata.query)
                )
            else:
                qset = Q()

            results = Bill.objects.filter(qset).order_by(order_key, '-bill_date').distinct()
        else:
            results = []

        paginator = Paginator(results, 3)
        page = request.GET.get('page')

        try:
            allbill = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            allbill = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            allbill = paginator.page(paginator.num_pages)

        context = { 'bill_list':allbill, }
        context = bills.make_context(qdata, context)
        return render(request, 'default/bill_list.html', context)

    @staticmethod
    def list(request, limit=0, order='-bill_date', filtering=None):

        qdata = bills.get_nav_list(request)

        order_key = order
        if qdata.order_key in ['location', 'pk', '-pk', 'bill_date', '-bill_date']:
            order_key = qdata.order_key

        bill_list = Bill.objects.order_by(order_key, '-bill_date').distinct()

        if limit>0:
            bill_list = bill_list[:limit]

        paginator = Paginator(bill_list, qdata.pageitems, orphans=2)
        page = request.GET.get('page')

        try:
            allbill = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            allbill = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            allbill = paginator.page(paginator.num_pages)

        context = { 'bill_list':allbill, }
        context = bills.make_context(qdata, context)

        return render(request, 'default/bill_list.html', context)


    @staticmethod
    def detail(request, bill_id):
        qdata = bills.get_nav_list(request)

        bill = get_object_or_404(Bill, pk=bill_id)

        context = {'bill': bill, }
        context = bills.make_context(qdata, context)
        return render(request, 'default/bill_detail.html', context)

    @staticmethod
    def add(request):
        qdata = bills.get_nav_list(request)

        if request.method == 'POST': # If the form has been submitted...
            form = BillEditForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                bill = Bill.objects.create()

                bill.bill_date    = form.cleaned_data['bill_date']

                bill.location = form.cleaned_data['location']

                bill.private_electricity_last    = form.cleaned_data['private_electricity_last']
                bill.private_electricity_current = form.cleaned_data['private_electricity_current']
                bill.private_electricity_bill    = form.cleaned_data['private_electricity_bill']

                bill.private_water_last    = form.cleaned_data['private_water_last']
                bill.private_water_current = form.cleaned_data['private_water_current']
                bill.private_water_bill    = form.cleaned_data['private_water_bill']

                bill.public_electricity          = form.cleaned_data['public_electricity']
                bill.public_water                = form.cleaned_data['public_water']
                bill.public_electricity_elevator = form.cleaned_data['public_electricity_elevator']
                bill.public_water_relay          = form.cleaned_data['public_water_relay']

                bill.property_cost            = form.cleaned_data['property_cost']
                bill.property_balance_last    = form.cleaned_data['property_balance_last']
                bill.property_balance_current = form.cleaned_data['property_balance_current']

                bill.save()

                # bill_id = bill.pk

                # return HttpResponseRedirect('/bills/%d' % bill_id) # Redirect after POST
                return HttpResponseRedirect('/bills/') # Redirect after POST
            else:
                context = {'form': form, }
                context = bills.make_context(qdata, context)
                return render(request, 'default/bill_edit.html', context )
        else:
            today_str = format(u"%s" % (date.today().isoformat()))

            default_values = {
                'bill_date'         : today_str,
                }
            form = BillEditForm(initial=default_values) # A form bound to the POST data

            context = { 'form': form, }
            context = bills.make_context(qdata, context)
            return render(request, 'default/bill_edit.html', context)

    @staticmethod
    def edit(request, bill_id):
        qdata = bills.get_nav_list(request)

        bill = get_object_or_404(Bill, pk=bill_id)
        if request.method == 'POST': # If the form has been submitted...
            form = BillEditForm(instance=bill, data=request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                Bill.objects.get(pk=bill_id)
                form.save()

                # return HttpResponseRedirect('/bills/'+bill_id) # Redirect after POST
                return HttpResponseRedirect('/bills/') # Redirect after POST
        else:
            form = BillEditForm(instance=bill)

            context = { 'form': form, 'bill': bill, }
            context = bills.make_context(qdata, context)
            return render(request, 'default/bill_edit.html', context)

        context = {'form': form, }
        context = bills.make_context(qdata, context)
        return render(request, 'default/bill_edit.html', context)

    @staticmethod
    def remove(request, bill_id):
        bill = get_object_or_404(Bill, pk=bill_id)
        #context = {'bill': bill}
        bill.delete()
        return HttpResponseRedirect('/bills/') # Redirect after POST

    @staticmethod
    def _export(request):
        if not os.path.exists('tmp/'):
            os.mkdir('tmp')
        for item in os.listdir('tmp/'):
            os.remove('tmp/'+item)
        filename = 'tmp/bills_export_%s.xml' % (date.today().strftime('%Y%m%d'))

        bill_ids = request.GET.get('id', '').strip().split(',')
        bill_ids = map(unicode.strip, filter(None, bill_ids))

        lines = utils.bills_export(bill_ids)
        lines.extend(utils.bills_export_other())
        utils.save_xml(lines, filename)
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper, content_type='application/octet-stream')
        # response['Content-Length'] = os.path.getsize(filename)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

        #return HttpResponseRedirect('/bills/') # Redirect after POST

    @staticmethod
    def _import(request, bill_ids):
        return HttpResponseRedirect('/bills/') # Redirect after POST


#
# FixedAsset actions
#
class locations:

    @staticmethod
    def list(request, limit=0):
        latest_location_list = FixedAsset.objects.order_by('description')

        if limit>0:
            context = {'location_list': latest_location_list[:limit]}
        else:
            context = {'location_list': latest_location_list}

        print context
        qdata = bills.get_nav_list(request)
        # context = {
        # }

        context = bills.make_context(qdata, context)
        return render(request, 'default/bills_location_list.html', context)

    @staticmethod
    def add(request):
        qdata = bills.get_nav_list(request)

        if request.method == 'POST':
            form = FixedAssetEditForm(request.POST)
            if form.is_valid():
                FixedAsset.objects.get_or_create(description=form.cleaned_data['description'])

                return HttpResponseRedirect('/bills/location/') # Redirect after POST
            else:
                context = {'form': form, }
        else:
            default_values = {
                'name'     : _('Unknown'),
                }
            form = FixedAssetEditForm(initial=default_values) # A form bound to the POST data
            context = {'form': form, }

        context = bills.make_context(qdata, context)
        return render(request, 'default/bills_location_edit.html', context )

    @staticmethod
    def edit(request, location_id):
        qdata = bills.get_nav_list(request)

        location = get_object_or_404(FixedAsset, pk=location_id)
        context = {'location': location}
        if request.method == 'POST':
            form = FixedAssetEditForm(instance=location, data=request.POST)
            if form.is_valid():
                form.save()

                return HttpResponseRedirect('/bills/location/') # Redirect after POST
            else:
                context = {'form': form,}
        else:
            form = FixedAssetEditForm(instance=location)
            context = {
                'form': form,
                'location': location,
                }

        context = bills.make_context(qdata, context)
        return render(request, 'default/bills_location_edit.html', context)

    @staticmethod
    def remove(request, location_id):
        location = get_object_or_404(FixedAsset, pk=location_id)
        #context = {'location': location}
        location.delete()
        return HttpResponseRedirect('/bills/location/') # Redirect after POST



class reports:
    class  report_item(object):
        pk    = None
        title = None
        mode  = None
        data  = None

    title_list = [_('Private Electricity'), _('Private Water'),
                  _('Public Electricity'), _('Public Water'),
                  _('Elevator'), _('Water Relay'), _('Property'),
                  _('Electricity Unitprice'), _('Electricity Count'),
                  _('Water Unitprice'), _('Water Count')]
    mode_list = ['bar', 'bar',
                 'bar', 'bar',
                 'bar', 'bar', 'bar',
                 'line', 'line',
                 'line', 'line']
    field_list = ['private_electricity_bill', 'private_water_bill',
                  'public_electricity', 'public_water',
                  'public_electricity_elevator', 'public_water_relay', 'property_cost',
                  'electricity_unitprice', 'electricity_count',
                  'water_unitprice', 'water_count']

    @staticmethod
    def list(request, limit=0):
        qdata = bills.get_nav_list(request)

        latest_report_list = []

        for idx in xrange(len(reports.title_list)):
            item = reports.report_item()
            item.pk    = idx
            item.title = reports.title_list[idx]
            item.mode  = reports.mode_list[idx]
            item.data  = None
            latest_report_list.append(item)

        if limit>0:
            context = {'report_list': latest_report_list[:limit]}
        else:
            context = {'report_list': latest_report_list}

        context = bills.make_context(qdata, context)
        return render(request, 'default/bills_report_list.html', context)

    @staticmethod
    def data_json(request, report_id):

        rData = dict()
        rData['cMode'] = ''
        rData['title']    = _('Unknown')
        rData['labels']   = []
        rData['tooltips'] = []
        rData['data']     = []

        id = int(report_id)
        if (0 <= id) and (id < 11):
            # print('Get private_electricity_bill data')
            if id < 7:
                items = Bill.objects.values('bill_date', reports.field_list[id]).order_by('bill_date')
                rData['title']    = reports.title_list[id]
                for value in items:
                    rData['cMode'] = str(reports.mode_list[id])
                    rData['labels'].append(value['bill_date'].strftime('%Y-%m'))
                    rData['data'].append(float(value[reports.field_list[id]]))
            else:
                items = Bill.objects.all().order_by('bill_date')
                rData['title']    = reports.title_list[id]
                for value in items:
                    value.calc()

                    rData['cMode'] = str(reports.mode_list[id])
                    rData['labels'].append(value.bill_date.strftime('%Y-%m'))
                    rData['data'].append(float(eval('value.' + reports.field_list[id])))

        # print(rData)


        result_data = json.dumps(rData)

        return HttpResponse(result_data)


#
# API of application
#
class api:
    @staticmethod
    def add_json(request):
        qdata = bills.get_nav_list(request)

        try:
            if request.method == 'POST': # If the form has been submitted...
                form = BillEditForm(request.POST)

                print('==================== AJAX POST ===================')

                if form.is_valid(): # All validation rules pass
                    print('==================== FORM Valid ===================')
                    # print(request.POST)
                    # Process the data in form.cleaned_data
                    # ...
                    bill = Bill.objects.create()
                    print('==================== Create new record ===================')

                    bill.bill_date                   = form.cleaned_data['bill_date']

                    bill.location                    = form.cleaned_data['location']

                    bill.private_electricity_last    = form.cleaned_data['private_electricity_last']
                    bill.private_electricity_current = form.cleaned_data['private_electricity_current']
                    bill.private_electricity_bill    = form.cleaned_data['private_electricity_bill']

                    bill.private_water_last          = form.cleaned_data['private_water_last']
                    bill.private_water_current       = form.cleaned_data['private_water_current']
                    bill.private_water_bill          = form.cleaned_data['private_water_bill']

                    bill.public_electricity          = form.cleaned_data['public_electricity']
                    bill.public_water                = form.cleaned_data['public_water']
                    bill.public_electricity_elevator = form.cleaned_data['public_electricity_elevator']
                    bill.public_water_relay          = form.cleaned_data['public_water_relay']

                    bill.property_cost               = form.cleaned_data['property_cost']
                    bill.property_balance_last       = form.cleaned_data['property_balance_last']
                    bill.property_balance_current    = form.cleaned_data['property_balance_current']

                    bill.save()

                    context = {'bill': bill, }
                    context = bills.make_context(qdata, context)
                    return render(request, 'default/bill_item.html', context)
                else:
                    print('==================== FORM not Valid ===================')
                    print(form.errors)
                    pass
            else:
                print('==================== Request Method Error ===================')
                pass
        except:
            pass

        rData = dict()
        rData['status'] = 'fail'
        jsonData = json.dumps(rData)
        # return HttpResponse(jsonData)
        return HttpResponse('fail')
        pass

    @staticmethod
    def test_json(request):
        try:
            if request.method == 'POST': # If the form has been submitted...
                print('==================== AJAX POST ===================')
                #print(request.body)
                #print('==================== AJAX POST ===================')



                print('==================== AJAX POST ===================')
            else:
                print('==================== AJAX GET ===================')
                print(request.GET)
                print('==================== AJAX GET ===================')
        except:
            print(request)
            pass

        rData = dict()

        result_data = json.dumps(rData)

        return HttpResponse(result_data)

# import models as bills_app
# post_syncdb.connect(index, sender=bills_app)

