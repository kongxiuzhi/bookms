@echo off

if not EXIST .\apps.db python manage.py syncdb --database=default
if not EXIST .\apps\apps.db python manage.py syncdb --database=apps
if not EXIST .\apps\books\apps.db python manage.py syncdb --database=books
if not EXIST .\apps\bills\apps.db python manage.py syncdb --database=bills
if not EXIST .\apps\bike\apps.db  python manage.py syncdb --database=bike

start python manage.py runserver
