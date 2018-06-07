# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from ip_proxy.connection.redis_connection import RedisConnection
from scrapy.exceptions import DropItem

class RedisPipeline(object):

    def __init__(self):
        conn = RedisConnection()
        self.pool = conn.pool
        pass

    def process_item(self, item, spider):
        conn = redis.Redis(connection_pool = self.pool)
        exist = conn.get(item['ip'])
        if exist:
            with open(LOG_PATH + time.strftime("%Y-%m-%d", time.localtime()) + '.redis.log', 'a') as f:
                f.write(item['ip'] + "\n")
            raise DropItem('ip:' + item['ip'] + 'existed')
        else:
            conn.set(item['ip'], 1)
            return item

