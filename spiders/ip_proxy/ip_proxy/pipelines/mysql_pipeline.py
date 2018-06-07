# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from ip_proxy.config import MYSQL,LOG_PATH
from twisted.enterprise import adbapi
import pymysql
import time
import json
import traceback

class MysqlPipeline(object):

    def __init__(self):
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


    def process_item(self, item, spider):
        res = self.dbpool.runInteraction(self.do_insert, item)
        res.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        with open(LOG_PATH + time.strftime("%Y-%m-%d", time.localtime()) + '.error.log', 'a') as f:
            failure.trap(Exception('insert failure'))
            f.write(traceback.format_exc())
        f.close()
        pass

    def do_insert(self, cursor, item):
        try:
            insert_sql, params = item.get_insert_sql()
            res = cursor.execute(insert_sql, params)
            if res != 1:
                raise Exception('insert error')
        except Exception as e:
            with open(LOG_PATH + time.strftime("%Y-%m-%d", time.localtime()) + '.error.log', 'a') as f:
                f.write('sql:' + insert_sql + "\n")
                f.write('params:' + json.dumps(params) + "\n")
                f.write(traceback.format_exc())
            f.close()
        
