# -*- coding: utf-8 -*-

from ip_proxy.config import MYSQL
from twisted.enterprise import adbapi
import pymysql
import logging
import traceback

# twisted adbapi连接
class MysqlConnection(object):

    def __init__(self):
        try:
            self.config = MYSQL
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
            logger = logging.getLogger()
            logger.error(traceback.format_exc)
            pass