#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'netcharm'

# Create your views here.

import os
from datetime import date

import json

from django.utils.translation import ugettext as _

from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404 #, get_list_or_404
from django.shortcuts import render
from django.http import HttpResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.core.servers.basehttp import FileWrapper

from django.db.models import Q

from models import Config, Book, Category, Location, State, Media, Statistic
from forms import ConfigEditForm, BookEditForm, CategoryEditForm, LocationEditForm, StateEditForm, MediaEditForm, StatisticEditForm

from douban import douban_book_image, douban_book_image_local
import utils

def index(request):
    return books.list(request, limit=20, order='-pk')


class uri_info:
    category_list = None
    location_list = None
    state_list    = None
    media_list    = None

    pubdate_list = None
    buydate_list = None

    tags_list = None

    path = None
    query = None
    filter_key = None
    filter_value = None
    order_key = None

    config = None

    theme = None
    pageitems = 20

    momo = None

#
# Configs
#
class configs:

    @staticmethod
    def set(request):
        name = request.GET.get('name', '').strip()
        value = request.GET.get('value', '').strip()

        if name:
            try:
                cfg = Config.objects.get(name=name)
                cfg.value = value
                cfg.save()
            # except:
            #     pass
            except ObjectDoesNotExist:
                cfg = Config.objects.get(name=name, value=value)
                # cfg.name = name
                # cfg.value = value
                cfg.save()

        return HttpResponseRedirect('/books/config/')

    @staticmethod
    def get(request, name=''):
        name = request.GET.get('name', name).strip()
        value = None
        if name:
            try:
                cfg = Config.objects.get(name=name)
                value = cfg.value
            except:
                pass
        else:
            pass

        return value
        #return HttpResponseRedirect('/books/config/')

    @staticmethod
    def list(request, limit=0):
        # latest_media_list = Media.objects.order_by('name')
        #
        # if limit>0:
        #     context = {'media_list': latest_media_list[:limit]}
        # else:
        #     context = {'media_list': latest_media_list}
        qdata = books.get_nav_list(request)

        latest_config_list = Config.objects.order_by('name')
        context = {
            'config_list': latest_config_list,
        }

        context = books.make_context(qdata, context)
        return render(request, 'default/config_list.html', context)

    @staticmethod
    def add(request):
        qdata = books.get_nav_list(request)
        if request.method == 'POST':
            form = ConfigEditForm(request.POST)
            if form.is_valid():
                item_name = form.cleaned_data['name']
                item_value = form.cleaned_data['value']
                try:
                    config = Config.objects.get(name=item_name)
                except ObjectDoesNotExist:
                    config = Config.objects.create(name=item_name)
                config.name = item_name
                config.value = item_value
                config.save()
                return HttpResponseRedirect('/books/config/')
            else:
                context ={'form': form, }
        else:
            default_values = {
                'name'     : _('Unknown'),
                }
            form = ConfigEditForm(initial=default_values)
            context = {'form': form, }

        context = books.make_context(qdata, context)
        return render(request, 'default/config_edit.html', context)

    @staticmethod
    def edit(request, config_id):
        qdata = books.get_nav_list(request)
        config = get_object_or_404(Config, name=config_id)
        if request.method == 'POST':
            form = ConfigEditForm(instance=config, data=request.POST)
            if form.is_valid():
                item_name = form.cleaned_data['name']
                item_value = form.cleaned_data['value']
                try:
                    # config = Config.objects.get(name=item_name)
                    config.name = item_name
                    config.value = item_value
                    config.save()
                except ObjectDoesNotExist:
                    form.save()

                return HttpResponseRedirect('/books/config/')
            else:
                context = {'form': form,}
        else:
            form = ConfigEditForm(instance=config)
            context = {'form': form, 'config': config, }

        context = books.make_context(qdata, context)
        return render(request, 'default/media_edit.html', context)

    @staticmethod
    def remove(request, config_id):
        config = get_object_or_404(Config, name=config_id)
        config.delete()
        return HttpResponseRedirect('/books/config/')


#
# Books Actions
#
class books:

    @staticmethod
    def get_nav_list(request):
        """

        :param request:
        :return:
        """
        q = uri_info()

        #import time
        #st = time.clock();

        q.category_list = Category.objects.order_by('name')
        q.location_list = Location.objects.order_by('name')
        q.state_list    = State.objects.order_by('name')
        q.media_list    = Media.objects.order_by('name')

        #print('Fetched datas : % 8.4fs' % (time.clock() - st))

        q.pubdate_list = []
        date_list = Book.objects.all().dates('pubdate', 'year')
        for years in date_list:
            q.pubdate_list.append(years.year)

        q.buydate_list = []
        date_list = Book.objects.all().dates('boughtdate', 'year')
        for years in date_list:
            q.buydate_list.append(years.year)

        #print('Fetched datas : % 8.4fs' % (time.clock() - st))

        tags_list = []
        tags_vlist = filter(None, Book.objects.values_list('read_tags', flat=True).order_by('read_tags'))
        tags_vlist = map(unicode.strip, tags_vlist)
        for tags_str in tags_vlist:
            tags = filter(None, tags_str.split(';'))
            tags = map(unicode.strip, tags)
            tags_list = list(set(tags_list+tags))
        q.tags_list = tags_list

        #print('Fetched datas : % 8.4fs' % (time.clock() - st))

        q.path = request.path
        q.query = request.GET.get('q', '').strip()
        q.filter_key = request.GET.get('f', '').strip()
        q.filter_value = request.GET.get('v', '').strip()
        q.order_key = request.GET.get('o', '').strip()

        q.theme = configs.get(request, 'theme')
        q.pageitems = configs.get(request, 'pageitems')
        q.pageitems =  q.pageitems if q.pageitems else 20

        q.momo = configs.get(request, 'momo')

        return  q

    @staticmethod
    def make_context(qdata, context):
        new_context = dict()
        for item in context:
            new_context[item] = context[item]

        new_context['category_list'] = qdata.category_list
        new_context['location_list'] = qdata.location_list
        new_context['pubdate_list']  = qdata.pubdate_list
        new_context['buydate_list']  = qdata.buydate_list
        new_context['state_list']    = qdata.state_list
        new_context['media_list']    = qdata.media_list
        new_context['tags_list']     = qdata.tags_list
        new_context['path']           = qdata.path
        new_context['query']          = qdata.query
        new_context['qkey']           = qdata.filter_key
        new_context['qvalue']         = qdata.filter_value
        new_context['order']          = qdata.order_key
        new_context['theme']          = qdata.theme
        if qdata.momo:
            new_context['momo']           = qdata.momo

        return new_context
        pass

    @staticmethod
    def search(request):
        qdata = books.get_nav_list(request)
        order_key = 'isbn13'
        if qdata.order_key:
            order_key = qdata.order_key

        if qdata.filter_key and qdata.filter_value:
            qf = Q()
            if   qdata.filter_key == 'pubdate':
                qf = Q(pubdate__year=qdata.filter_value)
            elif   qdata.filter_key == 'buydate':
                qf = Q(boughtdate__year=qdata.filter_value)
            elif qdata.filter_key == 'category':
                qf = Q(category__name__contains=qdata.filter_value)
            elif qdata.filter_key == 'location':
                qf = Q(location__name__contains=qdata.filter_value)
            elif qdata.filter_key == 'state':
                qf = Q(state__name__contains=qdata.filter_value)
            elif qdata.filter_key == 'media':
                qf = Q(media__name__contains=qdata.filter_value)
            elif qdata.filter_key == 'tag':
                qf = Q(read_tags__contains=qdata.filter_value)

            qset = qf & (
                Q(isbn13__icontains=qdata.query) |
                Q(title__icontains=qdata.query) |
                Q(summary__icontains=qdata.query) |
                Q(author__icontains=qdata.query) |
                Q(memo__icontains=qdata.query) |
                Q(read_tags__icontains=qdata.query) |
                Q(tags__icontains=qdata.query)
            )

            results = Book.objects.filter(qset).order_by(order_key).distinct()
        elif qdata.query:
            qset = (
                Q(isbn13__icontains=qdata.query) |
                Q(title__icontains=qdata.query) |
                Q(summary__icontains=qdata.query) |
                Q(author__icontains=qdata.query) |
                Q(memo__icontains=qdata.query) |
                Q(read_tags__icontains=qdata.query) |
                Q(tags__icontains=qdata.query)
            )
            results = Book.objects.filter(qset).order_by(order_key).distinct()
        else:
            results = []

        paginator = Paginator(results, 20)
        page = request.GET.get('page')

        try:
            allbook = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            allbook = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            allbook = paginator.page(paginator.num_pages)

        context = { 'book_list':allbook, }
        context = books.make_context(qdata, context)
        return render(request, 'default/book_list.html', context)

    @staticmethod
    def list(request, limit=0, order='isbn13', filtering=None):
        qdata = books.get_nav_list(request)

        order_key = order
        if qdata.order_key in ['title', 'isbn13', 'rating', '-rating', 'state', 'location', 'category', 'pk', '-pk', 'pubdate', '-pubdate', 'boughtdate', '-boughtdate']:
            order_key = qdata.order_key

        book_list = Book.objects.order_by(order_key).distinct()

        if limit>0:
            book_list = book_list[:limit]

        paginator = Paginator(book_list, qdata.pageitems, orphans=5)
        page = request.GET.get('page')

        try:
            allbook = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            allbook = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            allbook = paginator.page(paginator.num_pages)

        context = { 'book_list':allbook, }
        context = books.make_context(qdata, context)
        return render(request, 'default/book_list.html', context)

    @staticmethod
    def detail(request, book_id):
        qdata = books.get_nav_list(request)

        class bookface:
            face_l = ''
            face_m = ''
            face_s = ''

        book = get_object_or_404(Book, isbn13=book_id)

        bookface.face_l = douban_book_image_local(book.face_l, book.pubdate)
        bookface.face_m = douban_book_image_local(book.face_m, book.pubdate)
        bookface.face_s = douban_book_image_local(book.face_s, book.pubdate)

        #booknote = 'title\n===========\n* contenys'
        booknote = book.memo

        context = {'book': book, 'bookface': bookface, 'booknote': booknote, }
        context = books.make_context(qdata, context)
        return render(request, 'default/book_detail.html', context)

    @staticmethod
    def add(request):
        qdata = books.get_nav_list(request)

        if request.method == 'POST': # If the form has been submitted...
            form = BookEditForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                book_id = form.cleaned_data['isbn13']
                try:
                    Book.objects.get(isbn13=book_id)
                except ObjectDoesNotExist:
                    book = Book.objects.create()

                    book.isbn10       = form.cleaned_data['isbn10']
                    book.isbn13       = form.cleaned_data['isbn13']
                    book.face_l       = form.cleaned_data['face_l']
                    book.face_m       = form.cleaned_data['face_m']
                    book.face_s       = form.cleaned_data['face_s']
                    book.title        = form.cleaned_data['title']
                    book.subtitle     = form.cleaned_data['subtitle']
                    book.pages        = form.cleaned_data['pages']
                    book.author       = form.cleaned_data['author']
                    book.translator   = form.cleaned_data['translator']
                    book.publisher    = form.cleaned_data['publisher']
                    book.price        = form.cleaned_data['price']
                    book.boughtprice  = form.cleaned_data['boughtprice']
                    book.binding      = form.cleaned_data['binding']
                    book.pubdate      = form.cleaned_data['pubdate']
                    book.boughtdate   = form.cleaned_data['boughtdate']
                    book.author_intro = form.cleaned_data['author_intro']
                    book.summary      = form.cleaned_data['summary']
                    book.tags         = form.cleaned_data['tags']
                    book.rating       = form.cleaned_data['rating']
                    book.read_pages   = form.cleaned_data['read_pages']
                    book.read_start   = form.cleaned_data['read_start']
                    book.read_end     = form.cleaned_data['read_end']
                    book.read_tags    = form.cleaned_data['read_tags']
                    book.memo         = form.cleaned_data['memo']
                    book.state        = form.cleaned_data['state']
                    book.category     = form.cleaned_data['category']
                    book.location     = form.cleaned_data['location']
                    book.media        = form.cleaned_data['media']

                    book.save()

                    # Download book face
                    # noinspection PyBroadException
                    try:
                        douban_book_image(book.face_l, book.pubdate)
                        douban_book_image(book.face_m, book.pubdate)
                        douban_book_image(book.face_s, book.pubdate)
                    except:
                        pass

                return HttpResponseRedirect('/books/'+book_id) # Redirect after POST
            else:
                context = {'form': form, }
                context = books.make_context(qdata, context)
                return render(request, 'default/book_edit.html', context )
        else:
            default_values = {
                'isbn13'     : '',
                'title'      : _('Unknown'),
                'summery'    : _('Unknown'),
                'author'     : _('Unknown'),
                'boughtdate' : '2013-01-01',
                'publisher'  : _('Unknown'),
                'read_pages' : '0',
            }
            form = BookEditForm(initial=default_values) # A form bound to the POST data

            context = { 'form': form, }
            context = books.make_context(qdata, context)
            return render(request, 'default/book_edit.html', context)

    @staticmethod
    def add_multi(request):
        qdata = books.get_nav_list(request)

        default_values = {
            }
        form = BookEditForm(initial=default_values)
        location = form.fields['location'].widget.render('location', 'location', attrs={'id':'id_location', })
        category = form.fields['category'].widget.render('category', 'category', attrs={'id':'id_category', })
        media    = form.fields['media'].widget.render('media', 'media', attrs={'id':'id_media', })

        context = {'location': location,
                   'category': category,
                   'media'    : media,
                   }
        context = books.make_context(qdata, context)
        return render(request, 'default/book_add_multi.html', context)

    @staticmethod
    def edit(request, book_id):
        qdata = books.get_nav_list(request)

        book = get_object_or_404(Book, isbn13=book_id)
        if request.method == 'POST': # If the form has been submitted...
            form = BookEditForm(instance=book, data=request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                item_name = form.cleaned_data['isbn13']
                if item_name != book_id:
                    try:
                        Book.objects.get(isbn13=item_name)
                    except ObjectDoesNotExist:
                        form.save()
                        # Download book face
                        # noinspection PyBroadException
                        try:
                            douban_book_image(book.face_l, book.pubdate)
                            douban_book_image(book.face_m, book.pubdate)
                            douban_book_image(book.face_s, book.pubdate)
                        except:
                            pass
                else:
                    form.save()
                    # Download book face
                    # noinspection PyBroadException
                    try:
                        douban_book_image(book.face_l, book.pubdate)
                        douban_book_image(book.face_m, book.pubdate)
                        douban_book_image(book.face_s, book.pubdate)
                    except:
                        pass

                return HttpResponseRedirect('/books/'+book_id) # Redirect after POST
        else:
            form = BookEditForm(instance=book)

            context = { 'form': form, 'book': book, }
            context = books.make_context(qdata, context)
            return render(request, 'default/book_edit.html', context)

        context = {'form': form, }
        context = books.make_context(qdata, context)
        return render(request, 'default/book_edit.html', context)

    @staticmethod
    def note(request, book_id):
        book = get_object_or_404(Book, isbn13=book_id)


        #context = {'book': book}

        return HttpResponseRedirect('/books/'+book_id) # Redirect after POST

    @staticmethod
    def remove(request, book_id):
        book = get_object_or_404(Book, isbn13=book_id)
        #context = {'book': book}
        book.delete()
        return HttpResponseRedirect('/books/') # Redirect after POST

    @staticmethod
    def remove_multi(request):
        book_ids = request.GET.get('id', '').strip().split(',')
        book_ids = map(unicode.strip, filter(None, book_ids))
        for book_id in book_ids:
            # noinspection PyBroadException
            try:
                if len(book_id) == 13:
                    book = Book.objects.get(isbn13=book_id)
                    book.delete()
            except:
                pass
        return HttpResponseRedirect('/books/') # Redirect after POST
        #return HttpResponseRedirect(request.path) # Redirect after POST

    @staticmethod
    def change_state_multi(request):
        state = request.GET.get('v', '').strip()
        book_ids = request.GET.get('id', '').strip().split(',')
        book_ids = map(unicode.strip, filter(None, book_ids))
        for book_id in book_ids:
            # noinspection PyBroadException
            try:
                if len(book_id) == 13:
                    book = Book.objects.get(isbn13=book_id)
                    book.state = State.objects.get(name=state)
                    book.save()
            except:
                pass
        return HttpResponseRedirect('/books/') # Redirect after POST
        #return HttpResponseRedirect(request.path) # Redirect after POST

    @staticmethod
    def change_media_multi(request):
        media = request.GET.get('v', '').strip()
        book_ids = request.GET.get('id', '').strip().split(',')
        book_ids = map(unicode.strip, filter(None, book_ids))
        for book_id in book_ids:
            # noinspection PyBroadException
            try:
                if len(book_id) == 13:
                    book = Book.objects.get(isbn13=book_id)
                    book.media = Media.objects.get(name=media)
                    book.save()
            except:
                pass
        return HttpResponseRedirect('/books/') # Redirect after POST
        #return HttpResponseRedirect(request.path) # Redirect after POST

    @staticmethod
    def change_location_multi(request):
        location = request.GET.get('v', '').strip()
        book_ids = request.GET.get('id', '').strip().split(',')
        book_ids = map(unicode.strip, filter(None, book_ids))
        for book_id in book_ids:
            # noinspection PyBroadException
            try:
                if len(book_id) == 13:
                    book = Book.objects.get(isbn13=book_id)
                    book.location = Location.objects.get(name=location)
                    book.save()
            except:
                pass
        return HttpResponseRedirect('/books/') # Redirect after POST
        #return HttpResponseRedirect(request.path) # Redirect after POST

    @staticmethod
    def change_category_multi(request):
        category = request.GET.get('v', '').strip()
        book_ids = request.GET.get('id', '').strip().split(',')
        book_ids = map(unicode.strip, filter(None, book_ids))
        for book_id in book_ids:
            # noinspection PyBroadException
            try:
                if len(book_id) == 13:
                    book = Book.objects.get(isbn13=book_id)
                    book.category = Category.objects.get(name=category)
                    book.save()
            except:
                pass
        return HttpResponseRedirect('/books/') # Redirect after POST
        #return HttpResponseRedirect(request.path) # Redirect after POST

    @staticmethod
    def change_tag_multi(request):
        new_tags = request.GET.get('v', '').strip().split(',')
        book_ids = request.GET.get('id', '').strip().split(',')
        book_ids = map(unicode.strip, filter(None, book_ids))
        for book_id in book_ids:
            # noinspection PyBroadException
            try:
                if len(book_id) == 13:
                    book = Book.objects.get(isbn13=book_id)
                    tags = book.read_tags
                    for tag in new_tags:
                        ctag = tag.strip()
                        if len(ctag) == 0:
                            continue
                        elif tags is None:
                            tags = '%s' % ctag
                        elif tags.find(ctag) < 0:
                            tags = '%s ; %s' % (tags, ctag)
                    if book.read_tags != tags:
                        book.read_tags = tags
                        book.save()
                    print(book.read_tags)
            except:
                pass
        return HttpResponseRedirect('/books/') # Redirect after POST
        #return HttpResponseRedirect(request.path) # Redirect after POST

    @staticmethod
    def _export(request):
        if not os.path.exists('tmp/'):
            os.mkdir('tmp')
        for item in os.listdir('tmp/'):
            os.remove('tmp/'+item)
        filename = 'tmp/books_export_%s.xml' % (date.today().strftime('%Y%m%d'))

        book_ids = request.GET.get('id', '').strip().split(',')
        book_ids = map(unicode.strip, filter(None, book_ids))

        lines = utils.books_export(book_ids)
        lines.extend(utils.books_export_other())
        utils.save_xml(lines, filename)
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper, content_type='application/octet-stream')
        # response['Content-Length'] = os.path.getsize(filename)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

        #return HttpResponseRedirect('/books/') # Redirect after POST

    @staticmethod
    def _import(request, book_ids):
        return HttpResponseRedirect('/books/') # Redirect after POST

#
# Category actions
#
class categories:

    @staticmethod
    def list(request, limit=0):
        # latest_category_list = Category.objects.order_by('name')
        #
        # if limit>0:
        #     context = {'category_list': latest_category_list[:limit]}
        # else:
        #     context = {'category_list': latest_category_list}

        qdata = books.get_nav_list(request)
        context = { }
        context = books.make_context(qdata, context)
        return render(request, 'default/category_list.html', context)

    @staticmethod
    def add(request):
        qdata = books.get_nav_list(request)
        if request.method == 'POST':
            form = CategoryEditForm(request.POST)
            if form.is_valid():
                Category.objects.get_or_create(name=form.cleaned_data['name'])

                return HttpResponseRedirect('/books/category/')
            else:
                context = { 'form': form, }
        else:
            default_values = {
                'name'     : _('Unknown'),
                }
            form = CategoryEditForm(initial=default_values)
            context = { 'form': form, }

        context = books.make_context(qdata, context)
        return render(request, 'default/category_edit.html', context)

    @staticmethod
    def edit(request, category_id):
        qdata = books.get_nav_list(request)

        category = get_object_or_404(Category, name=category_id)
        context = {'category': category}
        if request.method == 'POST':
            form = CategoryEditForm(instance=category, data=request.POST)
            if form.is_valid():
                item_name = form.cleaned_data['name']
                try:
                    Category.objects.get(name=item_name)
                except ObjectDoesNotExist:
                    form.save()

                return HttpResponseRedirect('/books/category/') # Redirect after POST
            else:
                context = { 'form': form, }
        else:
            form = CategoryEditForm(instance=category)
            context = {
                'form': form,
                'category': category,
                }

        context = books.make_context(qdata, context)
        return render(request, 'default/category_edit.html', context)

    @staticmethod
    def remove(request, category_id):
        category = get_object_or_404(Category, name=category_id)
        #context = {'category': category}
        category.delete()
        return HttpResponseRedirect('/books/category/') # Redirect after POST


#
# Location actions
#
class locations:

    @staticmethod
    def list(request, limit=0):
        # latest_location_list = Location.objects.order_by('name')
        #
        # if limit>0:
        #     context = {'location_list': latest_location_list[:limit]}
        # else:
        #     context = {'location_list': latest_location_list}

        qdata = books.get_nav_list(request)
        context = {
            }

        context = books.make_context(qdata, context)
        return render(request, 'default/location_list.html', context)

    @staticmethod
    def add(request):
        qdata = books.get_nav_list(request)

        if request.method == 'POST':
            form = LocationEditForm(request.POST)
            if form.is_valid():
                Location.objects.get_or_create(name=form.cleaned_data['name'])

                return HttpResponseRedirect('/books/location/') # Redirect after POST
            else:
                context = {'form': form, }
        else:
            default_values = {
                'name'     : _('Unknown'),
                }
            form = LocationEditForm(initial=default_values) # A form bound to the POST data
            context = {'form': form, }

        context = books.make_context(qdata, context)
        return render(request, 'default/location_edit.html', context )

    @staticmethod
    def edit(request, location_id):
        qdata = books.get_nav_list(request)

        location = get_object_or_404(Location, name=location_id)
        context = {'location': location}
        if request.method == 'POST':
            form = LocationEditForm(instance=location, data=request.POST)
            if form.is_valid():
                item_name = form.cleaned_data['name']
                try:
                    Location.objects.get(name=item_name)
                except ObjectDoesNotExist:
                  form.save()

                return HttpResponseRedirect('/books/location/') # Redirect after POST
            else:
                context = {'form': form,}
        else:
            form = LocationEditForm(instance=location)
            context = {
                'form': form,
                'location': location,
                }

        context = books.make_context(qdata, context)
        return render(request, 'default/location_edit.html', context)

    @staticmethod
    def remove(request, location_id):
        location = get_object_or_404(Location, name=location_id)
        #context = {'location': location}
        location.delete()
        return HttpResponseRedirect('/books/location/') # Redirect after POST


#
# State actions
#
class states:

    @staticmethod
    def list(request, limit=0):
        # latest_state_list = State.objects.order_by('name')
        #
        # if limit>0:
        #     context = {'state_list': latest_state_list[:limit]}
        # else:
        #     context = {'state_list': latest_state_list}

        qdata = books.get_nav_list(request)
        context = {
            }

        context = books.make_context(qdata, context)
        return render(request, 'default/state_list.html', context)

    @staticmethod
    def add(request):
        qdata = books.get_nav_list(request)
        if request.method == 'POST':
            form = StateEditForm(request.POST)
            if form.is_valid():
                State.objects.get_or_create(name=form.cleaned_data['name'])
                return HttpResponseRedirect('/books/state/') # Redirect after POST
            else:
                context = {'form': form, }
        else:
            default_values = {
                'name'     : _('Unknown'),
                }
            form = StateEditForm(initial=default_values) # A form bound to the POST data
            context = {'form': form, }

        context = books.make_context(qdata, context)
        return render(request, 'default/state_edit.html', context)

    @staticmethod
    def edit(request, state_id):
        qdata = books.get_nav_list(request)
        state = get_object_or_404(State, name=state_id)
        if request.method == 'POST':
            form = StateEditForm(instance=state, data=request.POST)
            if form.is_valid():
                item_name = form.cleaned_data['name']
                try:
                    State.objects.get(name=item_name)
                except ObjectDoesNotExist:
                    form.save()

                return HttpResponseRedirect('/books/state/') # Redirect after POST
            else:
                context = {'form': form,}
        else:
            form = StateEditForm(instance=state)
            context = {'form': form, 'state': state, }

        context = books.make_context(qdata, context)
        return render(request, 'default/state_edit.html', context)

    @staticmethod
    def remove(request, state_id):
        state = get_object_or_404(State, name=state_id)
        #context = {'state': state}
        state.delete()
        return HttpResponseRedirect('/books/state/') # Redirect after POST

class medias:

    @staticmethod
    def list(request, limit=0):
        # latest_media_list = Media.objects.order_by('name')
        #
        # if limit>0:
        #     context = {'media_list': latest_media_list[:limit]}
        # else:
        #     context = {'media_list': latest_media_list}

        qdata = books.get_nav_list(request)
        context = {
            }

        context = books.make_context(qdata, context)
        return render(request, 'default/media_list.html', context)

    @staticmethod
    def add(request):
        qdata = books.get_nav_list(request)
        if request.method == 'POST':
            form = MediaEditForm(request.POST)
            if form.is_valid():
                Media.objects.get_or_create(name=form.cleaned_data['name'])
                return HttpResponseRedirect('/books/media/')
            else:
                context ={'form': form, }
        else:
            default_values = {
                'name'     : _('Unknown'),
                }
            form = MediaEditForm(initial=default_values)
            context = {'form': form, }

        context = books.make_context(qdata, context)
        return render(request, 'default/media_edit.html', context)

    @staticmethod
    def edit(request, media_id):
        qdata = books.get_nav_list(request)
        media = get_object_or_404(Media, name=media_id)
        if request.method == 'POST':
            form = MediaEditForm(instance=media, data=request.POST)
            if form.is_valid():
                item_name = form.cleaned_data['name']
                try:
                    Media.objects.get(name=item_name)
                except ObjectDoesNotExist:
                    form.save()

                return HttpResponseRedirect('/books/media/')
            else:
                context = {'form': form,}
        else:
            form = MediaEditForm(instance=media)
            context = {'form': form, 'media': media, }

        context = books.make_context(qdata, context)
        return render(request, 'default/media_edit.html', context)

    @staticmethod
    def remove(request, media_id):
        media = get_object_or_404(Media, name=media_id)
        #context = {'media': media}
        media.delete()
        return HttpResponseRedirect('/books/media/')


class reports:

    @staticmethod
    def list(request, limit=0):
        qdata = books.get_nav_list(request)

        latest_report_list = Statistic.objects.order_by('name')
        print(latest_report_list.count())
        if limit>0:
            context = {'report_list': latest_report_list[:limit]}
        else:
            context = {'report_list': latest_report_list}

        context = books.make_context(qdata, context)
        return render(request, 'default/statistic_list.html', context)

    @staticmethod
    def detail(request, report_id):
        qdata = books.get_nav_list(request)

        report = get_object_or_404(Statistic, name=report_id)

        styles = Statistic.STYLE_CHOICES
        fields = Statistic.FIELD_CHOICES
        rules  = Statistic.CONDITION_CHOICES


        context = { 'report': report, }
        context = books.make_context(qdata, context)
        return render(request, 'default/statistic_detail.html', context)

    @staticmethod
    def add(request):
        qdata = books.get_nav_list(request)
        if request.method == 'POST':
            form = StatisticEditForm(request.POST)
            if form.is_valid():
                item_name = form.cleaned_data['name']
                item_style = form.cleaned_data['style']
                item_setting = form.cleaned_data['setting']
                item_template = form.cleaned_data['template']
                try:
                    report = Statistic.objects.get(name=item_name)
                except ObjectDoesNotExist:
                    report = Statistic.objects.create(name=item_name)

                    report.name = item_name
                    report.style = item_style
                    report.setting = item_setting
                    report.template = item_template
                    report.save()

                return HttpResponseRedirect('/books/report/')
            else:
                context ={'form': form, }
        else:
            default_values = {
                'name'     : _('Unknown'),
                }
            form = StatisticEditForm(initial=default_values)
            context = {'form': form, }

        context = books.make_context(qdata, context)
        return render(request, 'default/statistic_edit.html', context)

    @staticmethod
    def edit(request, report_id):
        qdata = books.get_nav_list(request)
        report = get_object_or_404(Statistic, name=report_id)
        if request.method == 'POST':
            form = StatisticEditForm(instance=report, data=request.POST)
            if form.is_valid():
                item_name = form.cleaned_data['name']
                item_style = form.cleaned_data['style']
                item_setting = form.cleaned_data['setting']
                item_template = form.cleaned_data['template']
                try:
                    # report = Statistic.objects.get(name=item_name)
                    report.name = item_name
                    report.style = item_style
                    report.setting = item_setting
                    report.template = item_template
                    report.save()
                except ObjectDoesNotExist:
                    form.save()
                return HttpResponseRedirect('/books/report/')
            else:
                context = {'form': form,}
        else:
            form = StatisticEditForm(instance=report)
            context = {'form': form, 'report': report, }

        context = books.make_context(qdata, context)
        return render(request, 'default/statistic_edit.html', context)

    @staticmethod
    def remove(request, report_id):
        report = get_object_or_404(Statistic, name=report_id)
        print report_id
        #context = {'report': report}
        report.delete()
        return HttpResponseRedirect('/books/report/')

    @staticmethod
    def data(request, report_id=None):
        print 'args id=', report_id
        report_id = request.GET.get('name', report_id)
        print 'request id=', report_id

        jsonData = ''

        # print(report_id.encode('utf8'))
        # print(repr(report_id))
        try:
            report = Statistic.objects.get(name=report_id)
            chart_setting = eval( report.setting )
            # print 'chart_setting =', chart_setting
            field_names = chart_setting['field']
            # field_value =

            # print(field_names)
            field_name = 'pubdate' #field_names[0]
            # field_display = Book._get_FIELD_display(field_name)

        # field_counts = Book.objects.values(field_name).annotate(dcount=Count(field_name))

            pcs = []
            date_list = Book.objects.all().dates('pubdate', 'year')
            # print date_list, date_list.count()
            for years in date_list:
                result = Book.objects.filter(pubdate__year = years.year)
                # field_display = result.._get_FIELD_display(field_name)
                pcs.append((years.year, result.count()))

            rData = dict()
            rData['labels'] = []
            rData['tooltips'] = []
            rData['data'] = []
            for pc in pcs:
                rData['labels'].append(pc[0])
                rData['tooltips'].append(pc[0])
                rData['data'].append(pc[1])

            jsonData = json.dumps(rData)
        except ObjectDoesNotExist:
            print 'chart_setting =', 'not found'
            pass

        #return HttpResponse(result_data)
        return HttpResponse(jsonData)

    @staticmethod
    def data_xml(request, report_id=None):

        result_data = '''<?xml version="1.0" encoding="UTF-8" ?>
<graph caption="" xAxisName="" yAxisName="" decimalPrecision="0" formatNumberScale="0">
</graph>
        '''

        return HttpResponse(result_data)


#
# API of application
#
class api:
    ready = False
    isbnlist = []

    @staticmethod
    def test_json(request):
        try:
            if request.method == 'POST': # If the form has been submitted...
                print('==================== AJAX POST ===================')
                api.ready = False
                #print(request.body)
                #print('==================== AJAX POST ===================')
                booklist = utils.load_soap(request.body)

                api.isbnlist = []
                for book in booklist:
                    api.isbnlist.append(book['isbn'])

                utils.save_isbn(api.isbnlist)

                api.ready = True
                print('==================== AJAX POST ===================')
            else:
                print('==================== AJAX GET ===================')
                rData = dict()
                rData['status'] = 'fail'
                if api.ready:
                    rData['status'] = 'ok'
                    rData['isbnlist'] = '\n'.join(api.isbnlist)

                    api.ready = False
                    api.isbnlist = []

                result_data = json.dumps(rData)
                return HttpResponse(result_data)

                print('==================== AJAX GET ===================')
        except:
            print(request)
            pass


        rData = dict()
        result_data = json.dumps(rData)
        return HttpResponse(result_data)



