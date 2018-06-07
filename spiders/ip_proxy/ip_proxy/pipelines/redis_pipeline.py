# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from ip_proxy.config import REDIS,LOG_PATH
import time

class RedisPipeline(object):

    def __init__(self):
        self.config = REDIS
        self.pool = redis.ConnectionPool(host = self.config['host'], port = self.config['port'],
        db = self.config['db'], password = self.config['password'])
        pass

    def process_item(self, item, spider):
        conn = redis.Redis(connection_pool = self.pool)
        exist = conn.get(item['ip'])
        if exist:
            with open(LOG_PATH + time.strftime("%Y-%m-%d", time.localtime()) + '.redis.log', 'a') as f:
                f.write(item['ip'] + "\n")
            return item
        else:
            conn.set(item['ip'], 1)
            return item
