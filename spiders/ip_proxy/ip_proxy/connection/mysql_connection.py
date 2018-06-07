# -*- coding: utf-8 -*-

from ip_proxy.config import MYSQL,LOG_PATH
from twisted.enterprise import adbapi
import pymysql
import traceback

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
            with open(LOG_PATH + time.strftime("%Y-%m-%d", time.localtime()) + '.error.log', 'a') as f:
                f.write(traceback.format_exc)
            f.close