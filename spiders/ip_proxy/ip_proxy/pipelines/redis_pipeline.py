# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# redis过滤重复ip
from ip_proxy.connection.redis_connection import RedisConnection
from scrapy.exceptions import DropItem
import time
import logging

class RedisPipeline(object):

    def __init__(self):
        r = RedisConnection()
        self.conn = r.conn
        pass

    def process_item(self, item, spider):
        exist = self.conn.get(item['ip'])
        logger = logging.getLogger()
        if exist:
            logger.log(logging.DEBUG, 'ip:' + item['ip'] + 'existed')
            raise DropItem('ip:' + item['ip'] + 'existed')
        else:
            logger.log(logging.DEBUG, 'ip:' + item['ip'] + 'is new')
            self.conn.set(item['ip'], 1)
            return item

