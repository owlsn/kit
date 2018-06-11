# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 将ip存入mysql数据库
from ip_proxy.connection.mysql_connection import MysqlConnection
import time
import json
from ip_proxy.utils.log import log
import traceback
import copy

class MysqlPipeline(object):

    def __init__(self):
        conn = MysqlConnection()
        self.dbpool = conn.dbpool
        pass


    def process_item(self, item, spider):
        # 异步插入数据库,出现过重复插入问题,主要问题可能是多线程抓取情况下item参数传递问题,item内存地址相同
        # logger = log.getLogger('debug')
        # logger.debug(json.dumps(item))
        asyncItem = copy.deepcopy(item)
        res = self.dbpool.runInteraction(self.do_insert, asyncItem)
        res.addErrback(self.handle_error, asyncItem, spider)
        return item

    def handle_error(self, failure, item, spider):
        logger = log.getLogger('development')
        logger.error(str(failure))
        pass

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        try:
            res = cursor.execute(insert_sql, params)
            if res != 1:
                raise Exception('insert error')
        except Exception as e:
            logger = log.getLogger('development')
            logger.error('sql:' + insert_sql)
            logger.error('params:' + json.dumps(params))
            logger.error(traceback.format_exc())
            pass
        
