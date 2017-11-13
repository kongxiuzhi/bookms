# -*- coding: utf-8 -*-

__author__ = 'netcharm'

#######################

from django.conf.urls import patterns, url

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

import views
#from models import bike

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('apps.bike.views',
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
    # url(r'^config/$', views.configs.list, name='configs.list'),
    # url(r'^config/add/$', views.configs.add, name='configs.add'),
    # url(r'^config/(?P<config_id>(\w|\W)+)/edit/$', views.configs.edit, name='configs.edit'),
    # url(r'^config/(?P<config_id>(\w|\W)+)/remove/$', views.configs.remove, name='configs.remove'),
    # url(r'^config/get/$',views.configs.get, name='configs.get'),
    # url(r'^config/set/$',views.configs.set, name='configs.set'),

    # bike Actions
    # url(r'^search/$',views.bike.search, name='bike.search'),
    # url(r'^list/$', views.bike.list, name='bike.list'),
    # url(r'^add/$', views.bike.add, name='bike.add'),
    # url(r'^add-multi/$', views.bike.add_multi, name='bike.add_multi'),
    # url(r'^change-tag-multi/$', views.bike.change_tag_multi, name='bike.change_tag_multi'),
    # url(r'^change-media-multi/$', views.bike.change_media_multi, name='bike.change_media_multi'),
    # url(r'^change-state-multi/$', views.bike.change_state_multi, name='bike.change_state_multi'),
    # url(r'^change-location-multi/$', views.bike.change_location_multi, name='bike.change_location_multi'),
    # url(r'^change-category-multi/$', views.bike.change_category_multi, name='bike.change_category_multi'),
    # url(r'^remove-multi/$', views.bike.remove_multi, name='bike.remove_multi'),
    # url(r'^(?P<bike_id>\d+)/edit/$', views.bike.edit, name='bike.edit'),
    # url(r'^(?P<bike_id>\d+)/remove/$', views.bike.remove, name='bike.remove'),
    # url(r'^(?P<bike_id>\d+)/$', views.bike.detail, name='bike.detail'),
    # url(r'^export/$', views.bike._export, name='bike.export'),
    # url(r'^import/$', views.bike._import, name='bike.import'),

#    # State Actions
#    url(r'^state/$', views.states.list, name='states.list'),
#    url(r'^state/add/$', views.states.add, name='states.add'),
#    url(r'^state/(?P<state_id>(\w|\W)+)/edit/$', views.states.edit, name='states.edit'),
#    url(r'^state/(?P<state_id>(\w|\W)+)/remove/$', views.states.remove, name='states.remove'),

    # Statistic Actions
    # url(r'^report/$', views.reports.list, name='reports.list'),
    # url(r'^report/add/$', views.reports.add, name='reports.add'),
    # url(r'^report/data/$', views.reports.data, name='reports.data'),
    # url(r'^report/(?P<report_id>(\w|\W)+)/Data.xml/$', views.reports.data_xml, name='reports.data_xml'),
    # # url(r'^report/(?P<report_id>(\w|\W)+)/data/$', views.reports.data, name='reports.data'),
    # url(r'^report/(?P<report_id>(\w|\W)+)/edit/$', views.reports.edit, name='reports.edit'),
    # url(r'^report/(?P<report_id>(\w|\W)+)/remove/$', views.reports.remove, name='reports.remove'),
    # url(r'^report/(?P<report_id>(\w|\W)+)/$', views.reports.detail, name='reports.detail'),

)
