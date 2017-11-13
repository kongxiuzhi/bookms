# -*- coding: utf-8 -*-

__author__ = 'netcharm'

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

from django.conf import settings

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

import apps
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^apps/', include('apps.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    
    # customize url
    url(r'^$', views.home, name='apps.home'),

    # Config Actions
    url(r'^config/$', views.configs.list, name='configs.list'),
    url(r'^config/add/$', views.configs.add, name='configs.add'),
    url(r'^config/(?P<config_id>(\w|\W)+)/edit/$', views.configs.edit, name='configs.edit'),
    url(r'^config/(?P<config_id>(\w|\W)+)/remove/$', views.configs.remove, name='configs.remove'),
    url(r'^config/get/$',views.configs.get, name='configs.get'),
    url(r'^config/set/$',views.configs.set, name='configs.set'),

    # API url actions
    url(r'^api/app/add/$', views.api.add_json, name='api.add.app'),
    url(r'^api/app/(?P<app_id>\d+)/get/$', views.api.get_json, name='api.app.get'),
    url(r'^api/app/(?P<app_id>\d+)/edit/$', views.api.edit_json, name='api.app.edit'),
    url(r'^api/app/(?P<app_id>\d+)/remove/$', views.api.remove_json, name='api.app.remove'),

    # app op function
    url(r'^(?P<app_id>\d+)/remove/$', views.apps.remove, name='apps.remove'),


    # My Apps
    url(r'^books/', include('apps.books.urls')),
    url(r'^bike/', include('apps.bike.urls')),
    url(r'^bills/', include('apps.bills.urls')),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
