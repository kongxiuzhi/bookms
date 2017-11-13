# -*- coding: utf-8 -*-

__author__ = 'netcharm'

#######################


class AutoRouter(object):
    """
    A router to control all database operations on models in the
    'bills' application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read 'bills' models go to 'bills' db.
        """
        if model._meta.app_label == 'bills':
            return 'bills'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write 'bills' models go to 'bills' db.
        """
        if model._meta.app_label == 'bills':
            return 'bills'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the 'bills' app is involved.
        """
        if obj1._meta.app_label == 'bills' or \
           obj2._meta.app_label == 'bills':
            return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the 'bills' app only appears in the 'bills'
        database.
        """
        if db == 'bills':
            return model._meta.app_label == 'bills'
        elif model._meta.app_label == 'bills':
            return False
        return None
