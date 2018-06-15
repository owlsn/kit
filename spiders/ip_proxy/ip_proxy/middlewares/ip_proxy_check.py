# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from ip_proxy.utils.log import log
from ip_proxy.connection.redis_connection import RedisConnection
import socket
import struct
import json
import time
from ip_proxy.config import QUEUE_KEY

class IpProxyCheckBeginMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        r = RedisConnection(db = 1)
        self.conn = r.conn
        pass

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        level = request.meta.get('level')
        print(str(level))
        key = QUEUE_KEY + str(level)
        proxy = self.conn.lpop(key)
        if not proxy:
            return None
        logger = log.getLogger('debug')
        logger.info('redis push:{}'.format(proxy))
        ip = socket.inet_ntoa(struct.pack('I',socket.htonl(proxy['ip'])))
        port = str(proxy['port'])
        scheme = proxy['scheme']
        logger.info('ip:{},port:{}'.format(ip, port))
        request.meta['proxy'] = scheme + '://' + ip + ':' + port
        request.meta['ip'] = ip
        request.meta['port'] = port
        request.meta['start'] = int(time.time() * 1000)
        logger.info('start:{}'.format(int(time.time() * 1000)))
        return None

    def spider_opened(self, spider):
        pass

class IpProxyCheckEndMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_response(self, request, response, spider):
        delay = int(time.time() * 1000) - request.meta.get('start')
        level = request.meta['level']
        request.meta['delay'] = delay
        request.meta['level'] = level
        return response

    def spider_opened(self, spider):
        pass

