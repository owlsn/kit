# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# redis过滤重复ip
from ip_proxy.connection.redis_connection import redisDb0
from scrapy.exceptions import DropItem
import time
from ip_proxy.utils.log import log

class RedisPipeline(object):

    def __init__(self):
        self.conn = redisDb0.conn
        pass

    def process_item(self, item, spider):
        if ('ip' not in item.keys() and not item['ip']) or ('port' not in item.keys() and not item['port']):
            raise DropItem('ip or port is none')
        if not 'scheme' in item.keys() or not item['scheme']:
            item['scheme'] = 'http'
        key = item['scheme'] + ':' + item['ip'] + ':' + item['port']
        exist = self.conn.get(key)
        logger = log.getLogger('debug')
        if exist:
            # logger.debug('scheme:{},ip:{},port:{},is existed'.format(item['scheme'], item['ip'], item['port']))
            raise DropItem('ip:' + item['ip'] + 'existed')
        else:
            # logger.debug('scheme:{},ip:{},port:{},is new'.format(item['scheme'], item['ip'], item['port']))
            self.conn.set(key, 1)
            return item

