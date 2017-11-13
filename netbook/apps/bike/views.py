# -*- coding: utf-8 -*-

__author__ = 'netcharm'

#######################

# Create your views here.

from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse

def index(request):
    #return books.list(request, limit=20, order='-pk')
    return HttpResponseRedirect('/books')
