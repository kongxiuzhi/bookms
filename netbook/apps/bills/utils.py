# -*- coding: utf-8 -*-

__author__ = 'netcharm'

from models import Bill
from models import FixedAsset

from xml.dom.minidom import parseString, parse
from cgi import escape

import codecs
import json


def bill_add(bill_data, location=0, category=0, state=0):
    if bill_data is None:
        return

    bill = Bill.objects.create()

    if bill_data.has_key('bill_date' ):
        bill.bill_date    = bill_data['bill_date']

    if bill_data.has_key('state' ):
        bill.state        = State.objects.get_or_create(name=bill_data['state'])
    elif str(bill_state).isdigit() and int(bill_state)>0:
        bill.state        = State.objects.get_or_create(pk=int(bill_state))
    elif bill_state:
        bill.state        = State.objects.get_or_create(name=bill_state)

    if bill_data.has_key('category' ):
        bill.category     = Category.objects.get_or_create(name=bill_data['category'])
    elif str(bill_category).isdigit() and int(bill_category)>0:
        bill.category        = Category.objects.get_or_create(pk=int(bill_category))
    elif bill_category:
        bill.category     = Category.objects.get_or_create(name=bill_category)

    if bill_data.has_key('location' ):
        bill.location     = Location.objects.get_or_create(name=bill_data['location'])
    elif str(bill_location).isdigit() and int(bill_location)>0:
        bill.location        = Location.objects.get_or_create(pk=int(bill_location))
    elif bill_location:
        bill.location     = Location.objects.get_or_create(name=bill_location)

    bill.save()
    return bill
    pass


def bills_export(bill_ids=None):
    lines = []
    export_bill_list = []
    bills = Bill.objects.all()

    if bill_ids and (len(bill_ids) > 0):
        for bill in bills:
            if bill.isbn13 in bill_ids:
                export_bill_list.append(bill)
    else:
        for bill in bills:
            export_bill_list.append(bill)

    lines.append('  <bills>')
    for bill in export_bill_list:
        lines.append('    <bill>')
        lines.append('      <isbn10>%s</isbn10>'              % (bill.isbn10             if bill.isbn10 else ''))
        lines.append('      <isbn13>%s</isbn13>'              % (bill.isbn13             if bill.isbn13 else ''))
        lines.append('      <face_l>%s</face_l>'              % escape(bill.face_l       if bill.face_l else ''))
        lines.append('      <face_m>%s</face_m>'              % escape(bill.face_m       if bill.face_m else ''))
        lines.append('      <face_s>%s</face_s>'              % escape(bill.face_s       if bill.face_s else ''))
        lines.append('      <title>%s</title>'                % escape(bill.title        if bill.title else ''))
        lines.append('      <subtitle>%s</subtitle>'          % escape(bill.subtitle     if bill.subtitle else ''))
        lines.append('      <pages>%s</pages>'                % (bill.pages              if bill.pages else ''))
        lines.append('      <author>%s</author>'              % escape(bill.author       if bill.author else ''))
        lines.append('      <translator>%s</translator>'      % escape(bill.translator   if bill.translator else ''))
        lines.append('      <publisher>%s</publisher>'        % escape(bill.publisher    if bill.publisher else ''))
        lines.append('      <price>%s</price>'                % (bill.price              if bill.price else ''))
        lines.append('      <boughtprice>%s</boughtprice>'    % (bill.boughtprice        if bill.boughtprice else ''))
        lines.append('      <binding>%s</binding>'            % escape(bill.binding      if bill.binding else ''))
        lines.append('      <pubdate>%s</pubdate>'            % (bill.pubdate            if bill.pubdate else ''))
        lines.append('      <boughtdate>%s</boughtdate>'      % (bill.boughtdate         if bill.boughtdate else ''))
        lines.append('      <author_intro>%s</author_intro>'  % escape(bill.author_intro if bill.author_intro else ''))
        lines.append('      <summary>%s</summary>'            % escape(bill.summary      if bill.summary else ''))
        lines.append('      <tags>%s</tags>'                  % escape(bill.tags         if bill.tags else ''))
        lines.append('      <rating>%s</rating>'              % (bill.rating             if bill.rating else ''))
        lines.append('      <read_pages>%s</read_pages>'      % (bill.read_pages         if bill.read_pages else ''))
        lines.append('      <read_start>%s</read_start>'      % (bill.read_start         if bill.read_start else ''))
        lines.append('      <read_end>%s</read_end>'          % (bill.read_end           if bill.read_end else ''))
        lines.append('      <read_tags>%s</read_tags>'        % escape(bill.read_tags    if bill.read_tags else ''))
        lines.append('      <state>%s</state>'                % escape(bill.state.name        if bill.state_id>0 else ''))
        lines.append('      <category>%s</category>'          % escape(bill.category.name     if bill.category_id>0 else ''))
        lines.append('      <location>%s</location>'          % escape(bill.location.name     if bill.location_id>0 else ''))
        lines.append('      <media>%s</media>'                % escape(bill.media.name        if bill.media_id>0 else ''))
        lines.append('    </bill>')
    lines.append('  <bills>')


    return lines
    pass

def bills_export_other():
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

    return lines
    pass


def save_xml(lines, xml='bills.xml'):
    fxml = codecs.open(xml, mode='w', encoding='utf-8')

    fxml.writelines(['<?xml version="1.0" encoding="UTF-8"?>\n', '<library>\n'])
    fxml.writelines(map(lambda x:x+'\n', lines))
    fxml.writelines(['</library>\n\n'])

    fxml.close()

def load_xml(xml):
    dom = parse(xml)
    bill_list = dom.getElementsByTagName('bill')
    state_list = dom.getElementsByTagName('state')
    category_list = dom.getElementsByTagName('category')
    location_list = dom.getElementsByTagName('location')

    for state in state_list:
        item = []
        for child in state.childNodes:
            item.append(child.data)

        State.objects.get_or_create(name=''.join(item))

    pass


def bills_import(bill_ids=None):
    pass

if __name__ == '__main__':
    lines = bills_export(['9787810367141', '9787806658543', '9787563398836'])
    save_xml(lines, 'bills.xml')

