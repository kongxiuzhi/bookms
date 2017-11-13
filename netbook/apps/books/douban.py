# -*- coding: utf-8 -*-

__author__ = 'netcharm'

# import the logging library
# import logging
#
# # 创建一个logger
# # Get an instance of a logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
#
# # 创建一个handler，用于写入日志文件
# fh = logging.FileHandler('test.log')
# fh.setLevel(logging.DEBUG)
#
# # 定义handler的输出格式
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
#
# # 给logger添加handler
# logger.addHandler(fh)
#
#import logging

from django.conf import settings

from xml.dom.minidom import parseString
import requests
import urllib
import re
from os import path, makedirs
from datetime import date
import time
import json

def douban_book(isbn13):
    #isbn13 = isbn13.strip().encode('ascii')
    isbn13 = isbn13.encode('ascii')

    tags_text = ['title', 'name', 'summary']
    tags_attr = ['link', 'db:tag', 'db:attribute', 'gd:rating']
    data = dict()

    douban_url = r'https://api.douban.com/v2/book/isbn/'
    query_str = r'%s%s' % (douban_url, isbn13)
    headers = {
#      'Host':'api.douban.com',
      'Referer':'https://api.douban.com/',
      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Encoding':'gzip, deflate, br, compress',
      'Accept-Language':'zh,zh-CN;q=0.8,zh-TW;q=0.7,en;q=0.5,ja;q=0.3,zh-HK;q=0.2',
      'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/650.36 (KHTML, like Gecko) Chrome/198.0.2311.90 Safari/650.36'
    }
    resp = requests.get(query_str, headers = headers)
    info = resp.json()

#    resp = urllib.urlopen(query_str)
#    jstr = resp.read()
#    resp.close()
#    if len(jstr) < 20:
#        return None
#    info = json.loads(jstr, encoding='utf8')

#    print(resp.headers)
#    print(query_str)
#    print(info)

    if info.has_key('title'):
        data['title'] = info['title']
    if info.has_key('subtitle'):
        data['subtitle'] = info['subtitle']
    if info.has_key('origin_title"'):
        data['origin_title"'] = info['origin_title"']
    if info.has_key('alt_title"'):
        data['alt_title"'] = info['alt_title"']

    if info.has_key('author'):
        data['author'] = ' ; '.join(info['author'])
        data['name'] = data['author']
    if info.has_key('author_intro"'):
        data['author_intro"'] = info['author_intro"']
    if info.has_key('translator'):
        data['translator'] = ' ; '.join(info['translator'])

    if info.has_key('summary'):
        data['summary'] = info['summary']

    if info.has_key('catalog'):
        data['catalog'] = info['catalog']

    if info.has_key('url'):
        data['url'] = info['url']
    if info.has_key('alt'):
        data['alt'] = info['alt']
        data['alternate'] = info['alt']
    if info.has_key('ebook_url'):
        data['ebook_url'] = info['ebook_url']

    if info.has_key('id'):
        data['id'] = info['id']

    if info.has_key('isbn10'):
        data['isbn10'] = info['isbn10']
    if info.has_key('isbn13'):
        data['isbn13'] = info['isbn13']

    if info.has_key('binding'):
        data['binding'] = info['binding']

    if info.has_key('images'):
        if info['images'].has_key('small'):
            data['face_s'] = info['images']['small']
        if info['images'].has_key('medium'):
            data['face_m'] = info['images']['medium']
        if info['images'].has_key('large'):
            data['face_l'] = info['images']['large']

    if info.has_key('tags'):
        tags = []
        for tag in info['tags']:
          tags.append(u'%s(%d)' % (tag['title'], tag['count']))
        data['tags'] = ', '.join(tags)

    if info.has_key('rating'):
        #data['rating'] = u'%s(%d)' % (info['rating']['average'], info['rating']['numRaters'])
        data['rating'] = u'%s' % (info['rating']['average'])

    if info.has_key('pages'):
        data['pages'] = info['pages'].replace(u'页', '').strip()

    if info.has_key('price'):
        data['price'] = info['price'].replace(u'元', '').replace(u'CNY', '').strip()
    if info.has_key('ebook_price'):
        data['ebook_price'] = info['ebook_price'].replace(u'元', '').strip()

    if info.has_key('publisher'):
        data['publisher'] = info['publisher']
    if info.has_key('pubdate'):
        year  = 1970
        mouth = 1
        day   = 1

        # noinspection PyBroadException
        try:
            pds = []
            pd = info['pubdate'].replace('年', '-').replace('月', '-').replace('日', '-')
            if pd.find('-') > 0:
                pds = pd.split('-')
            elif pd.find('.') > 0:
                pds = pd.split('.')

            if len(pds)>=1:
                if len(pds[0]) >= 1:
                    year = int(pds[0])
            if len(pds)>=2:
                if len(pds[1]) >= 1:
                    mouth = int(pds[1])
            if len(pds)>=3:
                if len(pds[2]) >= 1:
                    day = int(pds[2])
        except:
            pass

        pdate = date(year, mouth, day)
        data['pubdate'] = pdate.strftime('%Y-%m-%d')
        #logging.debug(data['pubdate'])
        #print(data['pubdate'])

    return data

def douban_book_v1(isbn13):
    #print(isbn13)

    tags_text = ['title', 'name', 'summary']
    tags_attr = ['link', 'db:tag', 'db:attribute', 'gd:rating']
    data = dict()

    douban_url = 'https://api.douban.com/v2/book/isbn/'
    query_str = '%s%s' % (douban_url, isbn13.strip())
    xml = urllib.urlopen(query_str)

    #try:
    #dom = parse(xml)
    xmlstr = xml.read()
    xml.close()

    #print(xmlstr)
    if len(xmlstr) < 20:
        return None

    dom = parseString(xmlstr)

    for tag in tags_text:
        items = []
        for element in dom.getElementsByTagName(tag):
            item = []
            for child in element.childNodes:
                item.append(child.data)
            items.append(u' ; '.join(item))

        data[tag] = u' ; '.join(items)

    for element in dom.getElementsByTagName('link'):
        if element.hasAttribute('rel') and element.hasAttribute('href'):
            if element.attributes['rel'].value == 'image':
                face_s = element.attributes['href'].value
                face_m = face_s.replace('/spic/', '/mpic/')
                face_l = face_s.replace('/spic/', '/lpic/')

                data['face_s'] = face_s
                data['face_m'] = face_m
                data['face_l'] = face_l

    dbattrs = dict()
    for element in dom.getElementsByTagName('db:attribute'):
        if element.hasAttribute('name'):
            label = element.attributes['name'].value
            item = []
            for child in element.childNodes:
                item.append(child.data)
            content = u' ; '.join(item)
            if dbattrs.has_key(label):
                content = u'%s ; %s' % (dbattrs[label], content)
            dbattrs[str(label)] = content

            if content:
                data[label] = content.strip()
            else:
                data[label] = ''

    item = []
    for element in dom.getElementsByTagName('db:tag'):
        if element.hasAttribute('name'):
            item.append(element.attributes['name'].value)

    data['tags'] = u' ; '.join(item)

    item = []
    for element in dom.getElementsByTagName('gd:rating'):
        if element.hasAttribute('average'):
            item.append(element.attributes['average'].value)
            # if element.hasAttribute('numRaters'):
            #     item.append(element.attributes['numRaters'].value)

    if len(item)>0:
        data['rating'] = item[0]

    if data.has_key('pages' ):
        data['pages'] = data['pages'].replace(u'页', '').strip()

    if data.has_key('price' ):
        data['price'] = data['price'].replace(u'元', '').strip()

    if data.has_key('pubdate' ):
        year  = 1970
        mouth = 1
        day   = 1

        # noinspection PyBroadException
        try:
            pds = []
            pd = data['pubdate'].replace('年', '-').replace('月', '-').replace('日', '-')
            if pd.find('-') > 0:
                pds = pd.split('-')
            elif pd.find('.') > 0:
                pds = pd.split('.')

            if len(pds)>=1:
                if len(pds[0]) >= 1:
                    year = int(pds[0])
            if len(pds)>=2:
                if len(pds[1]) >= 1:
                    mouth = int(pds[1])
            if len(pds)>=3:
                if len(pds[2]) >= 1:
                    day = int(pds[2])
        except:
            pass

        pdate = date(year, mouth, day)
        data['pubdate'] = pdate.strftime('%Y-%m-%d')
        #logging.debug(data['pubdate'])
        #print(data['pubdate'])

    for item in data:
        if item:
            data[item] = data[item].strip()
        else:
            data[item] = ''

    return data

def douban_book_image(url, dest):
    if url and settings.MEDIA_ROOT:
        pubdate = u'misc'
        if dest:
            #pubdate = datetime.strptime(dest, '%Y-%m-%d').strftime('%Y-%m')
            pubdate = dest.strftime('%Y-%m')
        dest = u'%s/books/%s/' % ( settings.MEDIA_ROOT, pubdate )

        r = r'http:\/\/img\d+\.douban\.com'
        re_src = re.compile(r, re.I)
        image_dest = re_src.sub(dest, url).replace('//', '/')

        image_dir = image_dest.replace('/'+path.basename(image_dest), '')
        if not path.exists(image_dir):
            makedirs(image_dir, 0777)

        if not path.exists(image_dest):
            #print(image_dest)
            urllib.urlretrieve(url, image_dest)
    pass

def douban_book_image_local(url, dest):
    if url and settings.MEDIA_ROOT:
        pubdate = u'misc'
        if dest:
            pubdate = dest.strftime('%Y-%m')
        dest = u'%s/books/%s/' % ( settings.MEDIA_ROOT, pubdate )
        local = u'/media/books/%s/' % pubdate

        r = r'http:\/\/img\d+\.douban\.com'
        re_src = re.compile(r, re.I)
        image_dest = re_src.sub(dest, url).replace('//', '/')
        image_local = re_src.sub(local, url).replace('//', '/')

        if path.exists(image_dest):
            return image_local
    return url
