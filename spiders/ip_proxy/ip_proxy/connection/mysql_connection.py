# -*- coding: utf-8 -*-

from ip_proxy.config import MYSQL
from twisted.enterprise import adbapi
import pymysql
from ip_proxy.utils.log import Log
import traceback

# twisted adbapi连接
class MysqlConnection(object):

    def __init__(self, type = 'asyn'):
        try:
            self.config = MYSQL
            if type == 'syn':
                self.conn = pymysql.connect(
                    host = self.config['host'],
                    db = self.config['database'],
                    user = self.config['user'],
                    passwd = self.config['password'],
                    charset = self.config['charset'],
                    port = self.config['port']
                )
                pass
            else:
                dbparams = dict(
                    host = self.config['host'],
                    db = self.config['database'],
                    user = self.config['user'],
                    passwd = self.config['password'],
                    charset = self.config['charset'],
                    cursorclass = pymysql.cursors.DictCursor
                )
                self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
            pass
        except Exception as e:
            logger = Log().getLogger('development')
            logger.error(traceback.format_exc)
            pass