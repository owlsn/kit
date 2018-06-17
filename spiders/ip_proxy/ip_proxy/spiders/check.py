# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.connection.redis_connection import RedisConnection
from ip_proxy.utils.log import log
from ip_proxy.item.check_item import CheckItem
from scrapy.spidermiddlewares.httperror import HttpError
from ip_proxy.config import QUEUE_NUM
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from twisted.internet.error import TCPTimedOutError
import time
from ip_proxy.config import QUEUE_KEY

class CheckSpider(scrapy.Spider):
    name = 'check'
    allowed_domains = ['www.66ip.cn']
    base_url = 'http://www.66ip.cn/'

    def start_requests(self):
        for i in range(QUEUE_NUM):
            length = self.conn.llen(QUEUE_KEY + str(i))
            if length:
                self.level = i
                self.request = scrapy.Request(self.base_url, meta={'level':i}, callback=self.parse,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)
                yield self.request

    custom_settings = {
        'RETRY_ENABLED' : False,
        'RETRY_TIMES' : 2,
        'DOWNLOAD_TIMEOUT' : 60,
        'HTTPPROXY_AUTH_ENCODING' : 'utf-8',
        'CONCURRENT_REQUESTS' : 50,
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 50,
        'DOWNLOADER_MIDDLEWARES': {
            'ip_proxy.middlewares.random_user_agent.RandomUserAgentMiddleware' : 1002,
            'ip_proxy.middlewares.ip_proxy_check.IpProxyCheckBeginMiddleware': 1003,
            'ip_proxy.middlewares.ip_proxy_check.IpProxyCheckEndMiddleware': 1001,
        },
        'ITEM_PIPELINES': {
            'ip_proxy.pipelines.check_pipeline.CheckPipeline': 200,
        },
        'LOG_LEVEL' : 'INFO',
        'HTTPERROR_ALLOWED_CODES': range(200, 499)
    }

    def __init__(self):
        # redis连接,主要用于url判重
        r = RedisConnection(db = 1)
        self.conn = r.conn
        pass

    def parse(self, response):
        item = CheckItem()
        level = response.meta['level']
        item['delay'] = response.meta['delay']
        item['level'] = level
        item['ip'] = response.meta['proxy_ip']
        item['port'] = response.meta['proxy_port']
        item['scheme'] = response.meta['proxy_scheme']
        yield item
        length = self.conn.llen(QUEUE_KEY + str(level))
        if length:
            self.request = scrapy.Request(self.base_url, meta={'level':level}, callback=self.parse,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)
            yield self.request
        # logger = log.getLogger('development')
        # logger.info('parse result response:{},time:{}'.format(response, time.time()))
        pass
    
    def errback_httpbin(self, failure):
        item = CheckItem()
        level = self.request.meta['level']
        item['delay'] = -1
        item['level'] = level
        item['ip'] = self.request.meta['proxy_ip']
        item['port'] = self.request.meta['proxy_port']
        item['scheme'] = self.request.meta['proxy_scheme']
        yield item
        length = self.conn.llen(QUEUE_KEY + str(level))
        if length:
            self.request = scrapy.Request(self.base_url, meta={'level':level}, callback=self.parse,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)
            yield self.request
        # logger = log.getLogger('development')
        # logger.info('parse error:{},time:{},level:{},request.meta:{}'.format(failure, time.time(), self.level, self.request.meta))
        
        # in case you want to do something special for some errors,
        # you may need the failure's type:

        # if failure.check(HttpError):
        #     # these exceptions come from HttpError spider middleware
        #     # you can get the non-200 response
        #     response = failure.value.response
        #     self.logger.error('HttpError on %s', response.url)

        # elif failure.check(DNSLookupError):
        #     # this is the original request
        #     request = failure.request
        #     self.logger.error('DNSLookupError on %s', request.url)

        # elif failure.check(TimeoutError, TCPTimedOutError):
        #     request = failure.request
        #     self.logger.error('TimeoutError on %s', request.url)
        pass