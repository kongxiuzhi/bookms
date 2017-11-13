# -*- coding: utf-8 -*-

__author__ = 'netcharm'

#######################


class AutoRouter(object):
    """
    A router to control all database operations on models in the
    'bike' application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read 'bike' models go to 'bike' db.
        """
        if model._meta.app_label == 'bike':
            return 'bike'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write 'bike' models go to 'bike' db.
        """
        if model._meta.app_label == 'bike':
            return 'bike'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the 'bike' app is involved.
        """
        if obj1._meta.app_label == 'bike' or \
           obj2._meta.app_label == 'bike':
            return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the 'bike' app only appears in the 'bike'
        database.
        """
        if db == 'bike':
            return model._meta.app_label == 'bike'
        elif model._meta.app_label == 'bike':
            return False
        return None
