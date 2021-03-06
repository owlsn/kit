# -*- coding: utf-8 -*-

from ip_proxy.config import MYSQL
from twisted.enterprise import adbapi
import pymysql
from ip_proxy.utils.log import Log
import traceback

class MysqlAsyn(object):

    def __init__(self, *args, **kwargs):
        self.config = MYSQL
        self.connect(kwargs)

    def connect(self, *args, **kwargs):
        keys = kwargs.keys()
        logger = Log().getLogger('development')
        logger.info('connect')
        dbparams = dict(
                host = kwargs['host'] if 'host' in keys and kwargs['host'] else self.config['host'],
                db = kwargs['db'] if 'db' in keys and kwargs['db'] else self.config['database'],
                user = kwargs['user'] if 'user' in keys and kwargs['user'] else self.config['user'],
                passwd = kwargs['passwd'] if 'passwd' in keys and kwargs['passwd'] else self.config['password'],
                charset = kwargs['charset'] if 'charset' in keys and kwargs['charset'] else self.config['charset'],
                cursorclass=pymysql.cursors.DictCursor,
                cp_reconnect = True
            )
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        pass

    def close(self):
        logger = Log().getLogger('development')
        logger.info('close')
        if self.dbpool:
            self.dbpool.close()
            self.dbpool = None
        pass

class MysqlSyn(object):

    def __init__(self, *args, **kwargs):
        self.config = MYSQL
        self.connect(kwargs)

    def connect(self, *args, **kwargs):
        keys = kwargs.keys()
        logger = Log().getLogger('development')
        logger.info('connect')
        self.conn = pymysql.connect(
            host = kwargs['host'] if 'host' in keys and  kwargs['host'] else self.config['host'],
            db = kwargs['db'] if 'db' in keys and kwargs['db'] else self.config['database'],
            user = kwargs['user'] if 'user' in keys and kwargs['user'] else self.config['user'],
            passwd = kwargs['passwd'] if 'passwd' in keys and kwargs['passwd'] else self.config['password'],
            charset = kwargs['charset'] if 'charset' in keys and kwargs['charset'] else self.config['charset'],
            port = kwargs['port'] if 'port' in keys and kwargs['port'] else self.config['port']
        )
        pass

    def close(self):
        logger = Log().getLogger('development')
        logger.info('close')
        if self.conn:
            self.conn.close()
            self.conn = None
        pass

mysqlAsyn = MysqlAsyn()
mysqlSyn = MysqlSyn()