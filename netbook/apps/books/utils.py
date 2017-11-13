#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'netcharm'

from django.conf import settings
from django.utils.translation import ugettext as _

from models import Book
from models import Location
from models import Category
from models import Media
from models import State

from xml.dom.minidom import parseString, parse
from cgi import escape

from datetime import date, time, datetime
import codecs


def book_add(book_data, book_location=0, book_category=0, book_media=0, book_state=0):
    if book_data is None:
        return None

    book = Book.objects.create(isbn13=book_data['isbn13'], title=book_data['title'])

    memos = []
    if book_data.has_key('origin_title'):
        memos.append( _('Origin Title') + ': ' + book_data['origin_title'])
    if book_data.has_key('alt'):
        memos.append( _('Douban Link') + ': ' + book_data['alt'])

    if book_data.has_key('isbn10' ):
        book.isbn10       = book_data['isbn10']
    if book_data.has_key('isbn13' ):
        book.isbn13       = book_data['isbn13']
    if book_data.has_key('face_l' ):
        book.face_l       = book_data['face_l']
    if book_data.has_key('face_m' ):
        book.face_m       = book_data['face_m']
    if book_data.has_key('face_s' ):
        book.face_s       = book_data['face_s']
    if book_data.has_key('title' ):
        book.title        = book_data['title']
    if book_data.has_key('subtitle' ):
        book.subtitle     = book_data['subtitle']
    if book_data.has_key('pages' ):
        try:
            book.pages    = str(int(book_data['pages']))
        except:
            book.page     = 0
            #book.memo += '\n' + book_data['pages'] + '\n'
            memos.append(book_data['pages'])

        # if str(book_data['pages']).isdigit:
        #     book.pages    = book_data['pages']
        # else:
        #     book.summary += '\n' + book_data['pages'] + '\n'
    if book_data.has_key('author' ):
        book.author       = book_data['author']
    if book_data.has_key('translator' ):
        book.translator   = book_data['translator']
    if book_data.has_key('publisher' ):
        book.publisher    = book_data['publisher']
    if book_data.has_key('price' ):
        try:
            book.price    = str(float(book_data['price']))
        except:
            book.price    = '0.00'
            #book.memo += '\n' + book_data['price'] + '\n'
            memos.append(book_data['price'])

        # if str(book_data['price']).isdigit:
        #     book.price    = book_data['price']
        # else:
        #     book.summary += '\n' + book_data['price'] + '\n'
    if book_data.has_key('boughtprice' ):
        book.boughtprice  = book_data['boughtprice']
    if book_data.has_key('binding' ):
        book.binding      = book_data['binding']
    if book_data.has_key('pubdate' ):
        book.pubdate      = book_data['pubdate']
    if book_data.has_key('boughtdate' ):
        book.boughtdate   = book_data['boughtdate']
    if book_data.has_key('author-intro' ):
        book.author_intro = book_data['author-intro']
    if book_data.has_key('summary' ):
        book.summary      = book_data['summary']
    if book_data.has_key('tags' ):
        book.tags         = book_data['tags']
    if book_data.has_key('rating' ):
        book.rating       = book_data['rating']

    if book_data.has_key('state' ):
        book.state_id        = int(book_data['state'])
    elif str(book_state).isdigit() and int(book_state)>0:
        book.state_id        = int(book_state)
    elif book_state:
        book.state_id        = State.objects.get_or_create(name=book_state).pk;

    if book_data.has_key('category' ):
        book.category_id     = int(book_data['category'])
    elif str(book_category).isdigit() and int(book_category)>0:
        book.category_id     = int(book_category)
    elif book_category:
        book.category_id     = Category.objects.get_or_create(name=book_category).pk

    if book_data.has_key('location' ):
        book.location_id     = int(book_data['location'])
    elif str(book_location).isdigit() and int(book_location)>0:
        book.location_id     = int(book_location)
    elif book_location:
        book.location_id     = Location.objects.get_or_create(name=book_location).pk

    if book_data.has_key('media'):
        book.media_id        = int(book_data['media'])
    elif str(book_media).isdigit() and int(book_media)>0:
        book.media_id        = int(book_media)
    elif book_media:
        book.media_id        = Media.objects.get_or_create(name=book_media).pk

    book.memo = '\n'.join(memos)

    book.save()
    return book
    pass


def books_export(book_ids=None):
    lines = []
    export_book_list = []
    books = Book.objects.all()

    if book_ids and (len(book_ids) > 0):
        for book in books:
            if book.isbn13 in book_ids:
                export_book_list.append(book)
    else:
        for book in books:
            export_book_list.append(book)

    lines.append('  <books>')
    for book in export_book_list:
        lines.append('    <book>')
        lines.append('      <isbn10>%s</isbn10>'              % (book.isbn10             if book.isbn10 else ''))
        lines.append('      <isbn13>%s</isbn13>'              % (book.isbn13             if book.isbn13 else ''))
        lines.append('      <face_l>%s</face_l>'              % escape(book.face_l       if book.face_l else ''))
        lines.append('      <face_m>%s</face_m>'              % escape(book.face_m       if book.face_m else ''))
        lines.append('      <face_s>%s</face_s>'              % escape(book.face_s       if book.face_s else ''))
        lines.append('      <title>%s</title>'                % escape(book.title        if book.title else ''))
        lines.append('      <subtitle>%s</subtitle>'          % escape(book.subtitle     if book.subtitle else ''))
        lines.append('      <pages>%s</pages>'                % (book.pages              if book.pages else ''))
        lines.append('      <author>%s</author>'              % escape(book.author       if book.author else ''))
        lines.append('      <translator>%s</translator>'      % escape(book.translator   if book.translator else ''))
        lines.append('      <publisher>%s</publisher>'        % escape(book.publisher    if book.publisher else ''))
        lines.append('      <price>%s</price>'                % (book.price              if book.price else ''))
        lines.append('      <boughtprice>%s</boughtprice>'    % (book.boughtprice        if book.boughtprice else ''))
        lines.append('      <binding>%s</binding>'            % escape(book.binding      if book.binding else ''))
        lines.append('      <pubdate>%s</pubdate>'            % (book.pubdate            if book.pubdate else ''))
        lines.append('      <boughtdate>%s</boughtdate>'      % (book.boughtdate         if book.boughtdate else ''))
        lines.append('      <author_intro>%s</author_intro>'  % escape(book.author_intro if book.author_intro else ''))
        lines.append('      <summary>%s</summary>'            % escape(book.summary      if book.summary else ''))
        lines.append('      <tags>%s</tags>'                  % escape(book.tags         if book.tags else ''))
        lines.append('      <rating>%s</rating>'              % (book.rating             if book.rating else ''))
        lines.append('      <read_pages>%s</read_pages>'      % (book.read_pages         if book.read_pages else ''))
        lines.append('      <read_start>%s</read_start>'      % (book.read_start         if book.read_start else ''))
        lines.append('      <read_end>%s</read_end>'          % (book.read_end           if book.read_end else ''))
        lines.append('      <read_tags>%s</read_tags>'        % escape(book.read_tags    if book.read_tags else ''))
        lines.append('      <memo>%s</memo>'                  % escape(book.memo         if book.memo else ''))
        lines.append('      <state>%s</state>'                % escape(book.state.name        if book.state_id>0 else ''))
        lines.append('      <category>%s</category>'          % escape(book.category.name     if book.category_id>0 else ''))
        lines.append('      <location>%s</location>'          % escape(book.location.name     if book.location_id>0 else ''))
        lines.append('      <media>%s</media>'                % escape(book.media.name        if book.media_id>0 else ''))
        lines.append('    </book>')
    lines.append('  <books>')


    return lines
    pass

def books_export_other():
    lines = []

    lines.append('  <categories>')
    categories = Category.objects.all()
    for category in categories:
        lines.append('    <category>')
        lines.append('      <id>%s</id>'     % (category.id          if category.id else ''))
        lines.append('      <name>%s</name>' % escape(category.name if category.name else ''))
        lines.append('    </category>')
    lines.append('  <categories>')

    lines.append('  <locations>')
    locations = Location.objects.all()
    for location in locations:
        lines.append('    <location>')
        lines.append('      <id>%s</id>'     % (location.id          if location.id else ''))
        lines.append('      <name>%s</name>' % escape(location.name if location.name else ''))
        lines.append('    </location>')
    lines.append('  <locations>')

    lines.append('  <states>')
    states = State.objects.all()
    for state in states:
        lines.append('    <state>')
        lines.append('      <id>%s</id>'     % (state.id          if state.id else ''))
        lines.append('      <name>%s</name>' % escape(state.name if state.name else ''))
        lines.append('    </state>')
    lines.append('  <states>')

    lines.append('  <medias>')
    medias = Media.objects.all()
    for media in medias:
        lines.append('    <media>')
        lines.append('      <id>%s</id>'     % (media.id          if media.id else ''))
        lines.append('      <name>%s</name>' % escape(media.name if media.name else ''))
        lines.append('    </media>')
    lines.append('  <medias>')

    return lines
    pass


def save_xml(lines, xml='books.xml'):
    fxml = codecs.open(xml, mode='w', encoding='utf-8')

    fxml.writelines(['<?xml version="1.0" encoding="UTF-8"?>\n', '<library>\n'])
    fxml.writelines(map(lambda x:x+'\n', lines))
    fxml.writelines(['</library>\n\n'])

    fxml.close()

def load_xml(xml):
    dom = parse(xml)
    book_list = dom.getElementsByTagName('book')
    state_list = dom.getElementsByTagName('state')
    media_list = dom.getElementsByTagName('media')
    category_list = dom.getElementsByTagName('category')
    location_list = dom.getElementsByTagName('location')

    for state in state_list:
        item = []
        for child in state.childNodes:
            item.append(child.data)

        State.objects.get_or_create(name=''.join(item))

    pass


def books_import(book_ids=None):
    pass


def load_soap(xml):
    dom = parseString(xml)
    root = dom.documentElement
    # print(root.nodeName)

    datas = root.getElementsByTagName('data')
    data = datas[0].childNodes[0].nodeValue
    # print(data)

    dom_books = parseString(data).documentElement

    booklist = []
    bookObjlist = dom_books.getElementsByTagName('object-array')
    for bookObj in bookObjlist:
        bookinfos = []

        valuelist = bookObj.getElementsByTagName('string')
        for value in valuelist:
            for child in value.childNodes:
                # print("  >", child.nodeName, child.nodeType)
                if child.nodeType == 3:
                    bookinfos.append(child.data)

        if len(bookinfos) >=3:
            bookinfo = dict()
            bookinfo['isbn']      = bookinfos[0]
            bookinfo['count']     = bookinfos[1]
            bookinfo['scan_time'] = bookinfos[2]

            booklist.append(bookinfo)

            #print("ISBN: %s, Count: %s, ScanAt: %s" % ( bookinfo['isbn'], bookinfo['count'], bookinfo['scan_time'] ))

    return booklist
    pass

def save_isbn(isbnlist, path=None):

    if path:
        fn = '%s/books/isbn_%s.txt' % ( path, datetime.now().strftime('%Y%m%d%H%M%S') )
    else:
        fn = '%s/books/isbn_%s.txt' % ( settings.MEDIA_ROOT, datetime.now().strftime('%Y%m%d%H%M%S') )

    fn = fn.replace('//', '/')
    # print('fn: %s' % fn)
    # print('count: %d' % len(isbnlist))

    isbns = []
    for isbn in isbnlist:
        isbns.append(isbn + '\n')

    # print(isbns)

    fo = codecs.open(fn, 'wt')
    fo.writelines(isbns)
    fo.close()

    pass


if __name__ == '__main__':
    lines = books_export(['9787810367141', '9787806658543', '9787563398836'])
    save_xml(lines, 'books.xml')

