# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from ip_proxy.utils.log import log
from ip_proxy.connection.mysql_connection import MysqlConnection
import socket
import struct
import json
import time
from twisted.internet.error import (TimeoutError, TCPTimedOutError)

class IpProxyCheckBeginMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        c = MysqlConnection(type = 'syn')
        self.conn = c.conn
        pass

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        cursor = self.conn.cursor()
        sql = """select ip,port from `ip` limit 10,1"""
        cursor.execute(sql)
        res = cursor.fetchone()
        logger = log.getLogger('debug')
        logger.info('mysql select:' + json.dumps(res))
        ip = socket.inet_ntoa(struct.pack('I',socket.htonl(res[0])))
        port = str(res[1])
        logger.info('ip:{},port:{}'.format(res[0], port))
        request.meta['proxy'] = 'http://' + ip + ':' + port
        request.meta['ip'] = res[0]
        request.meta['port'] = port
        request.meta['start'] = int(time.time() * 1000)
        return None

    def process_exception(self, request, exception, spider):
        logger = log.getLogger('debug')
        logger.debug('begin exception: {}'.format(exception))
        pass

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
        delay = int(time.time() * 1000) - request.meta['start']
        request.meta['delay'] = delay
        return response

    def process_exception(self, request, exception, spider):
        logger = log.getLogger('debug')
        logger.debug('end exception: '.format(exception))
        pass

    def spider_opened(self, spider):
        pass

