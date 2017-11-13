# -*- coding: utf-8 -*-

__author__ = 'netcharm'

#######################


class AutoRouter(object):
    """
    A router to control all database operations on models in the
    'apps' application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read 'apps' models go to 'apps' db.
        """
        if model._meta.app_label == 'apps':
            return 'apps'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write 'apps' models go to 'apps' db.
        """
        if model._meta.app_label == 'apps':
            return 'apps'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the 'apps' app is involved.
        """
        if obj1._meta.app_label == 'apps' or \
           obj2._meta.app_label == 'apps':
            return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the 'apps' app only appears in the 'apps'
        database.
        """
        print(model._meta.app_label)
#        print(db)
        if db == 'apps':
            return model._meta.app_label == 'apps'
        elif model._meta.app_label == 'apps':
            return False
        return None
