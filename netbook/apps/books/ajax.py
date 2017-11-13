# -*- coding: utf-8 -*-

__author__ = 'netcharm'

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

from models import Book
from models import Location
from models import Category
from models import Media
from models import State
#from models import Statistic

import time

from douban import douban_book, douban_book_image

from utils import book_add, books_export

class ajax:
    progress = []
    finished = 0

@dajaxice_register
def get_progress(request):
    dajax = Dajax()

    if len(ajax.progress) > 0:
        data = '\n'.join( ajax.progress )
        data += '\n'
    else:
        # data = _('No Action')
        data = ""
    dajax.append('#id_ajax_progress', 'value', data)
    dajax.assign('#id_ajax_finished', 'value', int(ajax.finished*100))

    ajax.progress = []

    return dajax.json()


@dajaxice_register
def from_douban(request, book_id):
    dajax = Dajax()
    #print(book_id)
    book_data = douban_book(book_id)
    #print(book_data['title'])

    if book_data:
        if book_data.has_key('isbn10' ):
            dajax.assign('#id_isbn10'      , 'value', book_data['isbn10'      ])
        #if book_data.has_key('isbn13' ):
        #    dajax.assign('#id_isbn13'      , 'value', book_data['isbn13'      ])
        if book_data.has_key('face_l' ):
            dajax.assign('#id_face_l'      , 'value', book_data['face_l'      ])
        if book_data.has_key('face_m' ):
            dajax.assign('#id_face_m'      , 'value', book_data['face_m'      ])
        if book_data.has_key('face_s' ):
            dajax.assign('#id_face_s'      , 'value', book_data['face_s'      ])
        if book_data.has_key('title' ):
            dajax.assign('#id_title'       , 'value', book_data['title'       ])
        if book_data.has_key('subtitle' ):
            dajax.assign('#id_subtitle'    , 'value', book_data['subtitle'    ])
        if book_data.has_key('pages' ):
            dajax.assign('#id_pages'       , 'value', book_data['pages'       ])
        #if book_data.has_key('author' ):
        #    dajax.assign('#id_author'      , 'value', book_data['author'      ])
        if book_data.has_key('name' ):
            dajax.assign('#id_author'      , 'value', book_data['name'        ])
        if book_data.has_key('translator' ):
            dajax.assign('#id_translator'  , 'value', book_data['translator'  ])
        if book_data.has_key('publisher' ):
            dajax.assign('#id_publisher'   , 'value', book_data['publisher'   ])
        if book_data.has_key('price' ):
            dajax.assign('#id_price'       , 'value', book_data['price'       ])
        if book_data.has_key('binding' ):
            dajax.assign('#id_binding'     , 'value', book_data['binding'     ])
        if book_data.has_key('pubdate' ):
            dajax.assign('#id_pubdate'     , 'value', book_data['pubdate'     ])
        if book_data.has_key('author-intro' ):
            dajax.assign('#id_author_intro', 'value', book_data['author-intro'])
        if book_data.has_key('summary' ):
            dajax.assign('#id_summary'     , 'value', book_data['summary'     ])
        if book_data.has_key('tags' ):
            dajax.assign('#id_tags'        , 'value', book_data['tags'        ])
        if book_data.has_key('rating' ):
            dajax.assign('#id_rating'      , 'value', book_data['rating'      ])
    else:
        dajax.assign('#id_title'      , 'value',  _(u'No Douban result'))

    return dajax.json()

@dajaxice_register
def from_douban_multi(request, book_ids, book_location, book_category, book_media):
    dajax = Dajax()

    count = len(book_ids)
    index = 0.

    result = dict()
    result_failed = dict()
    for book_id in book_ids:
        ajax.finished = index / count
        index += 1.0

        #time.sleep(0.1)

        if len(book_id) != 13:
            result[book_id] = _(u'%s length less 13') % ''
            result_failed[book_id] = result[book_id]
            ajax.progress.append('%s : %s' % (book_id, result[book_id]))
            continue
        if not book_id.isdigit():
            result[book_id] = _(u'%s not a digit') % ''
            result_failed[book_id] = result[book_id]
            ajax.progress.append('%s : %s' % (book_id, result[book_id]))
            continue

        try:
            Book.objects.get(isbn13=book_id)
            result[book_id] =  _(u'%s Exists') % ''
            ajax.progress.append('%s : %s' % (book_id, result[book_id]))
        except ObjectDoesNotExist:
            time.sleep(0.5)

            book_data = douban_book(book_id)

            if book_data is None:
                result[book_id] =  _(u'No Douban result')
                result_failed[book_id] = result[book_id]
                ajax.progress.append('%s : %s' % (book_id, result[book_id]))
                continue

            if book_data['isbn13'] != book_id:
                result[book_id] =  _(u'Fuzzy with Douban result(%s)') % book_data['isbn13']
                result_failed[book_id] = result[book_id]
                ajax.progress.append('%s : %s' % (book_id, result[book_id]))
                continue

            book = book_add(book_data, book_location, book_category, book_media)

            # Download book face
            # noinspection PyBroadException
            try:
                douban_book_image(book.face_l, book.pubdate)
                douban_book_image(book.face_m, book.pubdate)
                douban_book_image(book.face_s, book.pubdate)
            except:
                pass

            result[book_id] = _('Add Success')
            ajax.progress.append('%s : %s' % (book_id, result[book_id]))

    data_result = []
    for key in result:
        data_result.append('%s : %s\n' % (key, result[key]))

    data_failed = []
    for key in result_failed:
        data_failed.append('%s : %s\n' % (key, result_failed[key]))

    # if len(data_result) > 0:
    #     data = ''.join(data_result)
    # else:
    #     data = _('No Action')
    # dajax.assign('#id_result', 'value', ''.join(data))

    if len(data_failed) > 0:
        data = ''.join(data_failed)
    else:
        data = _('No Error')

    dajax.assign('#id_result_failed', 'value', data)

    ajax.finished = 1.00
    return dajax.json()


@dajaxice_register
def change_state(request, book_selector, book_id, book_state):
    dajax = Dajax()

    # noinspection PyBroadException
    try:
        book = Book.objects.get(isbn13=book_id)

        state = State.objects.get(name=book_state)

        book.state = state

        book.save()

        dajax.assign(book_selector, 'value', book.state)
    except:
        pass

    return dajax.json()

@dajaxice_register
def change_location(request, book_selector, book_id, book_location):
    dajax = Dajax()

    # noinspection PyBroadException
    try:
        book = Book.objects.get(isbn13=book_id)

        location = Location.objects.get(name=book_location)

        book.location = location

        book.save()

        dajax.assign(book_selector, 'value', book.location)
    except:
        pass

    return dajax.json()

@dajaxice_register
def export_books(request, book_ids=None):

    # book_ids = filter(None, book_ids.split(','))
    # book_ids = map(unicode.strip, tags)

    books_export(book_ids)
    pass
