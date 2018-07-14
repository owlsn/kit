# -*- coding: utf-8 -*-

from ip_proxy.config import MYSQL
from twisted.enterprise import adbapi
import pymysql
from ip_proxy.utils.log import log
import traceback

# twisted adbapi连接
class MysqlConnection(object):

    def __init__(self):
        self.config = MYSQL

    def get_instance(self, *args, **kwargs):
        keys = kwargs.keys()
        self.type = 'syn' if 'type' in keys and kwargs['type'] == 'syn' else 'asyn'
        if not hasattr(self, 'conn') or not self.conn:
            logger = log.getLogger('development')
            logger.info('connect')
            self.connect(kwargs)
        return self
        pass

    def connect(self, *args, **kwargs):
        keys = kwargs.keys()
        if self.type == 'syn':
            self.conn = pymysql.connect(
                host = kwargs['host'] if 'host' in keys and  kwargs['host'] else self.config['host'],
                db = kwargs['db'] if 'db' in keys and kwargs['db'] else self.config['database'],
                user = kwargs['user'] if 'user' in keys and kwargs['user'] else self.config['user'],
                passwd = kwargs['passwd'] if 'passwd' in keys and kwargs['passwd'] else self.config['password'],
                charset = kwargs['charset'] if 'charset' in keys and kwargs['charset'] else self.config['charset'],
                port = kwargs['port'] if 'port' in keys and kwargs['port'] else self.config['port']
            )
        else:
            dbparams = dict(
                host = kwargs['host'] if 'host' in keys and kwargs['host'] else self.config['host'],
                db = kwargs['db'] if 'db' in keys and kwargs['db'] else self.config['database'],
                user = kwargs['user'] if 'user' in keys and kwargs['user'] else self.config['user'],
                passwd = kwargs['passwd'] if 'passwd' in keys and kwargs['passwd'] else self.config['password'],
                charset = kwargs['charset'] if 'charset' in keys and kwargs['charset'] else self.config['charset'],
                cursorclass = pymysql.cursors.DictCursor
            )
            self.conn = adbapi.ConnectionPool('pymysql', **dbparams)
        pass

    def close(self):
        logger = log.getLogger('development')
        logger.info('close')
        if self.conn:
            self.conn.close()
            self.conn = None
        pass

mysql = MysqlConnection()