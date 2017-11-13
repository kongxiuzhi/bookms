# -*- coding: utf-8 -*-

__author__ = 'netcharm'

from django.conf.urls import patterns, url

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

import views
#from models import Book

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('apps.books.views',
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

    # Book Actions
    url(r'^search/$',views.books.search, name='books.search'),
    url(r'^list/$', views.books.list, name='books.list'),
    url(r'^add/$', views.books.add, name='books.add'),
    url(r'^add-multi/$', views.books.add_multi, name='books.add_multi'),
    url(r'^change-tag-multi/$', views.books.change_tag_multi, name='books.change_tag_multi'),
    url(r'^change-media-multi/$', views.books.change_media_multi, name='books.change_media_multi'),
    url(r'^change-state-multi/$', views.books.change_state_multi, name='books.change_state_multi'),
    url(r'^change-location-multi/$', views.books.change_location_multi, name='books.change_location_multi'),
    url(r'^change-category-multi/$', views.books.change_category_multi, name='books.change_category_multi'),
    url(r'^remove-multi/$', views.books.remove_multi, name='books.remove_multi'),
    url(r'^(?P<book_id>\d+)/edit/$', views.books.edit, name='books.edit'),
    url(r'^(?P<book_id>\d+)/remove/$', views.books.remove, name='books.remove'),
    url(r'^(?P<book_id>\d+)/note/$', views.books.note, name='books.note'),
    url(r'^(?P<book_id>\d+)/$', views.books.detail, name='books.detail'),
    url(r'^export/$', views.books._export, name='books.export'),
    url(r'^import/$', views.books._import, name='books.import'),

    # # Music Actions
    # url(r'^music/$', views.music.list, name='music.list'),
    # url(r'^music/add/$', views.music.add, name='music.add'),
    # url(r'^music/(?P<music_id>(\w|\W)+)/edit/$', views.music.edit, name='music.edit'),
    # url(r'^music/(?P<music_id>(\w|\W)+)/remove/$', views.music.remove, name='music.remove'),
    #
    # # Movie Actions
    # url(r'^movie/$', views.movie.list, name='movie.list'),
    # url(r'^movie/add/$', views.movie.add, name='movie.add'),
    # url(r'^movie/(?P<movie_id>(\w|\W)+)/edit/$', views.movie.edit, name='movie.edit'),
    # url(r'^movie/(?P<movie_id>(\w|\W)+)/remove/$', views.movie.remove, name='movie.remove'),

    # Category Actions
    url(r'^category/$', views.categories.list, name='categories.list'),
    url(r'^category/add/$', views.categories.add, name='categories.add'),
    url(r'^category/(?P<category_id>(\w|\W)+)/edit/$', views.categories.edit, name='categories.edit'),
    url(r'^category/(?P<category_id>(\w|\W)+)/remove/$', views.categories.remove, name='categories.remove'),

    # Location Actions
    url(r'^location/$', views.locations.list, name='locations.list'),
    url(r'^location/add/$', views.locations.add, name='locations.add'),
    url(r'^location/(?P<location_id>(\w|\W)+)/edit/$', views.locations.edit, name='locations.edit'),
    url(r'^location/(?P<location_id>(\w|\W)+)/remove/$', views.locations.remove, name='locations.remove'),

    # State Actions
    url(r'^state/$', views.states.list, name='states.list'),
    url(r'^state/add/$', views.states.add, name='states.add'),
    url(r'^state/(?P<state_id>(\w|\W)+)/edit/$', views.states.edit, name='states.edit'),
    url(r'^state/(?P<state_id>(\w|\W)+)/remove/$', views.states.remove, name='states.remove'),

    # Media Actions
    url(r'^media/$', views.medias.list, name='medias.list'),
    url(r'^media/add/$', views.medias.add, name='medias.add'),
    url(r'^media/(?P<media_id>(\w|\W)+)/edit/$', views.medias.edit, name='medias.edit'),
    url(r'^media/(?P<media_id>(\w|\W)+)/remove/$', views.medias.remove, name='medias.remove'),

    # Statistic Actions
    url(r'^report/$', views.reports.list, name='reports.list'),
    url(r'^report/add/$', views.reports.add, name='reports.add'),
    url(r'^report/data/$', views.reports.data, name='reports.data'),
    url(r'^report/(?P<report_id>(\w|\W)+)/Data.xml/$', views.reports.data_xml, name='reports.data_xml'),
    # url(r'^report/(?P<report_id>(\w|\W)+)/data/$', views.reports.data, name='reports.data'),
    url(r'^report/(?P<report_id>(\w|\W)+)/edit/$', views.reports.edit, name='reports.edit'),
    url(r'^report/(?P<report_id>(\w|\W)+)/remove/$', views.reports.remove, name='reports.remove'),
    url(r'^report/(?P<report_id>(\w|\W)+)/$', views.reports.detail, name='reports.detail'),

    # API url actions
    url(r'^api/test/$', views.api.test_json, name='views.api.test'),

)
