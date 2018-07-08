# -*- coding: utf-8 -*-

from ip_proxy.config import MYSQL
from twisted.enterprise import adbapi
import pymysql
from ip_proxy.utils.log import log
import traceback

# twisted adbapi连接
class MysqlConnection(object):

    def __init__(self, type = 'asyn', host = None, db = None, user = None, passwd = None, charset = None, port = None):
        try:
            self.config = MYSQL
            if type == 'syn':
                self.conn = pymysql.connect(
                    host = host if host else self.config['host'],
                    db = db if db else self.config['database'],
                    user = user if user else self.config['user'],
                    passwd = passwd if passwd else self.config['password'],
                    charset = charset if charset else self.config['charset'],
                    port = port if port else self.config['port']
                )
            else:
                dbparams = dict(
                    host = host if host else self.config['host'],
                    db = db if db else self.config['database'],
                    user = user if user else self.config['user'],
                    passwd = passwd if passwd else self.config['password'],
                    charset = charset if charset else self.config['charset'],
                    cursorclass = pymysql.cursors.DictCursor
                )
                self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
            pass
        except Exception as e:
            logger = log.getLogger('development')
            logger.error(traceback.format_exc)
            pass

mysqlSyn = MysqlConnection(type = 'syn')