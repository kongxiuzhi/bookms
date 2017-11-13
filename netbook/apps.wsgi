# -*- coding: utf-8 -*-

import os
import sys

if not os.path.dirname(__file__) in sys.path[:1]:
    sys.path.insert(0, os.path.dirname(__file__))
    #sys.path.append(os.path.dirname(__file__))

#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['DJANGO_SETTINGS_MODULE'] = 'apps.settings'
os.environ["LANG"] = "zh_CN.utf8" 

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
