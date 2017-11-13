# -*- coding: utf-8 -*-

__author__ = 'netcharm'

class AutoRouter(object):
    """
    A router to control all database operations on models in the
    'books' application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read 'books' models go to 'books' db.
        """
        if model._meta.app_label == 'books':
            return 'books'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write 'books' models go to 'books' db.
        """
        if model._meta.app_label == 'books':
            return 'books'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the 'books' app is involved.
        """
        if obj1._meta.app_label == 'books' or \
           obj2._meta.app_label == 'books':
            return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the 'books' app only appears in the 'books'
        database.
        """
        if db == 'books':
            return model._meta.app_label == 'books'
        elif model._meta.app_label == 'books':
            return False
        return None
