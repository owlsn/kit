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
import time
from ip_proxy.config import QUEUE_KEY
from scrapy.exceptions import IgnoreRequest

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
        if level is None:
            raise IgnoreRequest
        key = QUEUE_KEY + str(level)
        length = self.conn.llen(key)
        if not length:
            raise IgnoreRequest
        byte = self.conn.lpop(key)
        d_str = str(byte, encoding = "utf-8")  
        data = eval(d_str)
        if not data['ip'] or not data['port']:
            raise IgnoreRequest
        scheme = data['scheme'] if data['scheme'] is not None else 'http'
        ip = socket.inet_ntoa(struct.pack('I',socket.htonl(int(data['ip']))))
        port = data['port']
        proxy = scheme + '://' + ip + ':' + str(port)
        request.meta['proxy'] = proxy
        request.meta['begin'] = time.time() * 1000
        request.meta['proxy_ip'] = data['ip']
        request.meta['proxy_port'] = data['port']
        request.meta['proxy_scheme'] = data['scheme']
        # logger = log.getLogger('development')
        # logger.info('begin middleware start, request.meta:{},time:{}'.format(request.meta, time.time()))
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
        if response.status == 200:
            delay = time.time() * 1000 - int(request.meta['begin'])
            request.meta['delay'] = delay
            response.request_meta = request.meta
            # logger = log.getLogger('development')
            # logger.info('end middleware start, request.meta:{},response:{},time:{}'.format(request.meta, response.request_meta, time.time()))
            return response
        else:
            raise IgnoreRequest
            pass

    def spider_opened(self, spider):
        pass

