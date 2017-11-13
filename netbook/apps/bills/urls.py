# -*- coding: utf-8 -*-

__author__ = 'netcharm'

#######################

from django.conf.urls import patterns, url

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

import views
import utils

#from models import bills

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('apps.bills.views',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^apps/', include('apps.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # Home List
    url(r'^$', views.index, name='index'),

    # Config Actions
    url(r'^config/$', views.configs.list, name='configs.list'),
    url(r'^config/add/$', views.configs.add, name='configs.add'),
    url(r'^config/(?P<config_id>(\w|\W)+)/edit/$', views.configs.edit, name='configs.edit'),
    url(r'^config/(?P<config_id>(\w|\W)+)/remove/$', views.configs.remove, name='configs.remove'),
    url(r'^config/get/$',views.configs.get, name='configs.get'),
    url(r'^config/set/$',views.configs.set, name='configs.set'),

    # bills Actions
    url(r'^search/$',views.bills.search, name='bills.search'),
    url(r'^list/$', views.bills.list, name='bills.list'),
    url(r'^add/$', views.bills.add, name='bills.add'),
    url(r'^(?P<bill_id>\d+)/edit/$', views.bills.edit, name='bills.edit'),
    url(r'^(?P<bill_id>\d+)/remove/$', views.bills.remove, name='bills.remove'),
    url(r'^(?P<bill_id>\d+)/$', views.bills.detail, name='bills.detail'),
    url(r'^export/$', views.bills._export, name='bills.export'),
    url(r'^import/$', views.bills._import, name='bills.import'),

    # Fixed Assets Actions
    url(r'^location/$', views.locations.list, name='bill.locations.list'),
    url(r'^location/add/$', views.locations.add, name='bill.locations.add'),
    url(r'^location/(?P<location_id>(\w|\W)+)/edit/$', views.locations.edit, name='bill.locations.edit'),
    url(r'^location/(?P<location_id>(\w|\W)+)/remove/$', views.locations.remove, name='bill.locations.remove'),

    # Statistic Actions
    url(r'^report/$', views.reports.list, name='bill.reports.list'),
    url(r'^report/(?P<report_id>(\w|\W)+)/data/$', views.reports.data_json, name='bill.reports.data'),

    # API url actions
    url(r'^api/add/bill/$', views.api.add_json, name='views.api.add.bill'),
    url(r'^api/test/$', views.api.test_json, name='views.api.test'),


)
