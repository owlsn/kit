# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# redis过滤重复ip
from ip_proxy.connection.redis_connection import RedisConnection
from scrapy.exceptions import DropItem
from ip_proxy.config import LOG_PATH
import time

class RedisPipeline(object):

    def __init__(self):
        r = RedisConnection()
        self.conn = r.conn
        pass

    def process_item(self, item, spider):
        exist = self.conn.get(item['ip'])
        if exist:
            with open(LOG_PATH + time.strftime("%Y-%m-%d", time.localtime()) + '.redis_exist.log', 'a') as f:
                f.write(item['ip'] + "\n")
            raise DropItem('ip:' + item['ip'] + 'existed')
        else:
            with open(LOG_PATH + time.strftime("%Y-%m-%d", time.localtime()) + '.redis.log', 'a') as f:
                f.write(item['ip'] + "\n")
            self.conn.set(item['ip'], 1)
            return item

