#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qingyun.meng on 15/6/30.
"""
peewee Database Manager
setting like this:
DATABASE = {
    'default': {
        'name': 'test',
        'engine': 'MySQLDatabase',
        # 'pool': 'PooledMySQLDatabase',
        'pool_args': {
            'max_connections': 20,
            'stale_timeout': 200
        },
        'host': '127.0.0.1',
        'passwd': '',
        'echo': True

    }
}
"""
import sys
import peewee
from peewee import Model, ImproperlyConfigured
from playhouse.read_slave import ReadSlaveModel
from playhouse.shortcuts import RetryOperationalError

def load_class(s):
    path, klass = s.rsplit('.', 1)
    __import__(path)
    mod = sys.modules[path]
    return getattr(mod, klass)

class DBManager(object):
    def __init__(self, setting, name='default', database=None, replica=()):
        self.setting = setting
        self.database = database
        self.name = name
        self.replica = replica

        if self.database is None:
            self.load_setting()

        if self.replica:
            self.Model = self.get_replica_model_class()
        else:
            self.Model = self.get_model_class()

    def load_setting(self):
        database_config = dict(self.setting[self.name])
        replica = None
        if 'master' in database_config:
            master = database_config['master']
            replica = database_config['replica'] if 'replica' in database_config else None
        else:
            master = database_config

        self.database = self.load_database(master)
        if replica:
            self.replica = tuple([self.load_database(rep_setting) for rep_setting in replica])

    def load_database(self, setting):
        try:
            database_name = setting.pop('name')
            echo_sql = setting.pop('echo', False)

            if echo_sql:
                self.set_echo()

            engine = setting.pop('engine', None)
            pool = setting.pop('pool', None)
            pool_args = setting.pop('pool_args', {})

        except KeyError:
            raise ImproperlyConfigured('Please specify a "name" and "engine" for your database')

        wrap_retry_handler = lambda dbclass_name, dbclass: type("Retry%s" % dbclass_name,
                                                                (RetryOperationalError, dbclass,),
                                                                {
                                                                    '__module__': dbclass.__module__
                                                                })

        if pool:
            pool_class = load_class("playhouse.pool.%s" % pool) if pool else None

            try:

                dbpool = wrap_retry_handler(pool, pool_class)(database_name,
                                                              max_connections=pool_args.get('max_connections', 20),
                                                              stale_timeout=pool_args.get('stale_timeout', None),
                                                              **setting)
                return dbpool
            except ImportError:
                raise ImproperlyConfigured('Unable to import pool class: "%s"' % pool)
        else:
            try:
                database_class = load_class('peewee.%s' % engine)
                assert issubclass(database_class, peewee.Database)

            except ImportError:
                raise ImproperlyConfigured('Unable to import: "%s"' % engine)
            except AttributeError:
                raise ImproperlyConfigured('Database engine not found: "%s"' % engine)
            except AssertionError:
                raise ImproperlyConfigured('Database engine not a subclass of peewee.Database: "%s"' % engine)
            return wrap_retry_handler(engine, database_class)(database_name, **setting)

    def set_echo(self):
        import logging

        logger = logging.getLogger('peewee')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler())

    def get_model_class(self):
        class BaseModel(Model):
            class Meta:
                database = self.database

        return BaseModel

    def get_replica_model_class(self):
        class BaseModel(ReadSlaveModel):
            class Meta:
                database = self.database
                read_slaves = self.replica

        return BaseModel

    def connect_db(self, database=None):
        if database:
            database.connect()
        else:
            self.database.connect()

    def close_db(self, database=None):
        if not database:
            database = self.database

        if not database.is_closed():
            database.close()

    def close_all(self):
        self.close_db(self.database)
        for rep in self.replica:
            self.close_db(rep)
