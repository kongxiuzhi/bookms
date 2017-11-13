# -*- coding: utf-8 -*-

__author__ = 'netcharm'

# Create your views here.

import os
from datetime import date

import json

from django.http import HttpResponse

from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404 #, get_list_or_404
from django.shortcuts import render

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils.translation import ugettext as _

from models import Config, App
from forms import ConfigEditForm, AppEditForm


def home(request):
    return apps.list(request, limit=20, order='name')
    # return HttpResponse("Hello, world. You're at the apps home.")


class uri_info:
    app_root = ''
    app_name = _('My Apps')

    location_list = None

    app_year_list = None
    app_month_list = None
    buydate_list = None

    tags_list = None

    path = None
    query = None
    filter_key = None
    filter_value = None
    order_key = None

    config = None
    formAddApp = None

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

        return HttpResponseRedirect('/apps/config/')

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
        qdata = apps.get_nav_list(request)

        latest_config_list = Config.objects.order_by('key')
        context = {
            'config_list': latest_config_list,
            }

        context = apps.make_context(qdata, context)
        return render(request, 'default/apps_config_list.html', context)

    @staticmethod
    def add(request):
        qdata = apps.get_nav_list(request)
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
                return HttpResponseRedirect('/config/')
            else:
                context ={'form': form, }
        else:
            default_values = {
                'key'     : _('Unknown'),
                }
            form = ConfigEditForm(initial=default_values)
            context = {'form': form, }

        context = apps.make_context(qdata, context)
        return render(request, 'default/apps_config_edit.html', context)

    @staticmethod
    def edit(request, config_id):
        qdata = apps.get_nav_list(request)
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

                return HttpResponseRedirect('/apps/config/')
            else:
                context = {'form': form,}
        else:
            form = ConfigEditForm(instance=config)
            context = {'form': form, 'config': config, }

        context = apps.make_context(qdata, context)
        return render(request, 'default/media_edit.html', context)

    @staticmethod
    def remove(request, config_id):
        config = get_object_or_404(Config, key=config_id)
        config.delete()
        return HttpResponseRedirect('/apps/config/')


#
# Apps Actions
#
class apps:

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
            }
        q.formAddApp = AppEditForm(initial=default_values) # A form bound to the POST data

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

        new_context['form_add'] = qdata.formAddApp

        new_context['path']     = qdata.path
        new_context['query']    = qdata.query
        new_context['qkey']     = qdata.filter_key
        new_context['qvalue']   = qdata.filter_value
        new_context['order']    = qdata.order_key
        new_context['theme']    = qdata.theme

        return new_context
        pass

    @staticmethod
    def list(request, limit=0, order='name', filtering=None):

        qdata = apps.get_nav_list(request)

        order_key = order
        if qdata.order_key in ['pk', '-pk', 'name', '-name']:
            order_key = qdata.order_key

        app_list = App.objects.order_by(order_key, 'pk').distinct()

        if limit>0:
            app_list = app_list[:limit]

        paginator = Paginator(app_list, qdata.pageitems, orphans=2)
        page = request.GET.get('page')

        try:
            allapp = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            allapp = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            allapp = paginator.page(paginator.num_pages)

        context = { 'app_list':allapp, }
        context = apps.make_context(qdata, context)

        return render(request, 'default/apps_list.html', context)


    @staticmethod
    def remove(request, app_id):
        app = App.objects.get(pk=app_id)
        app.delete()
        return HttpResponseRedirect('/') # Redirect after POST

#
# API of application
#
class api:
    @staticmethod
    def add_json(request):
        try:
            if request.method == 'POST': # If the form has been submitted...
                form = AppEditForm(request.POST)

                print('==================== AJAX POST ===================')

                if form.is_valid(): # All validation rules pass
                    print('==================== FORM Valid ===================')
                    # print(request.POST)
                    # Process the data in form.cleaned_data
                    # ...
                    app = App.objects.create()

                    print('==================== Create new record ===================')

                    app.name        = form.cleaned_data['name']
                    app.description = form.cleaned_data['description']
                    app.url         = form.cleaned_data['url']
                    app.icon        = form.cleaned_data['icon']

                    app.save()

                    context = {'app': app, }
                    return render(request, 'default/apps_item.html', context)
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
    def edit_json(request, app_id):
        print("=================================")

        try:
            if request.method == 'POST': # If the form has been submitted...
                form = AppEditForm(request.POST)

                print('==================== AJAX POST ===================')

                if form.is_valid(): # All validation rules pass
                    print('==================== FORM Valid ===================')
                    # print(request.POST)
                    # Process the data in form.cleaned_data
                    # ...
                    app = App.objects.get(pk=app_id)

                    print('==================== Edit record ===================')

                    app.name        = form.cleaned_data['name']
                    app.description = form.cleaned_data['description']
                    app.url         = form.cleaned_data['url']
                    app.icon        = form.cleaned_data['icon']

                    app.save()

                    rData = dict()
                    rData['app_id'] = app_id
                    rData['name'] = app.name
                    rData['description'] = app.description
                    rData['url'] = app.url
                    rData['icon'] = app.icon

                    jsonData = json.dumps(rData)
                    return HttpResponse(jsonData)
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
    def get_json(request, app_id):

        app = App.objects.get(pk=app_id)

        rData = dict()
        rData['appid'] = app_id
        rData['name'] = app.name
        rData['description'] = app.description
        rData['url'] = app.url
        rData['icon'] = app.icon

        jsonData = json.dumps(rData)
        return HttpResponse(jsonData)

    @staticmethod
    def remove_json(request, app_id):

        app = App.objects.get(pk=app_id)
        app.delete()

        rData = dict()
        rData['status'] = 'ok'

        jsonData = json.dumps(rData)
        return HttpResponse(jsonData)
