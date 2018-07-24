# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.utils.log import Log
from ip_proxy.item.check_item import CheckItem
from scrapy.spidermiddlewares.httperror import HttpError
from ip_proxy.config import QUEUE_NUM, CHECK_URL
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
import time
from ip_proxy.config import QUEUE_KEY, QUEUE_NUM, CHECK_URL
from ip_proxy.spiders.base import BaseSpider

class CheckSpider(BaseSpider):
    name = 'check'
    # 用于检验代理可用性的网站
    base_url = CHECK_URL

    def start_requests(self):
        # 对应level的url放入对应的队列，而url的leve是由delay确定
        for i in range(QUEUE_NUM):
            length = self.conn.llen(QUEUE_KEY + str(i))
            if length:
                self.level = i
                self.request = scrapy.Request(self.base_url, meta={'level':i}, priority = (QUEUE_NUM - i), callback=self.parse,
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

    def parse(self, response):
        item = CheckItem()
        level = response.meta['level']
        item['times'] = response.meta['times']
        item['delay'] = response.meta['delay']
        item['level'] = level
        item['ip'] = response.meta['proxy_ip']
        item['port'] = response.meta['proxy_port']
        item['scheme'] = response.meta['proxy_scheme']
        yield item
        for i in range(QUEUE_NUM):
            length = self.conn.llen(QUEUE_KEY + str(i))
            if length:
                self.request = scrapy.Request(self.base_url, meta={'level':i}, priority = (QUEUE_NUM - i), callback=self.parse,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)
                yield self.request
        # logger = Log().getLogger('development')
        # logger.info('parse result response:{},time:{}'.format(response, time.time()))
        pass
    
    def errback_httpbin(self, failure):
        item = CheckItem()
        level = self.request.meta['level']
        item['delay'] = -1
        item['times'] = self.request.meta['times']
        item['level'] = 0
        item['ip'] = self.request.meta['proxy_ip']
        item['port'] = self.request.meta['proxy_port']
        item['scheme'] = self.request.meta['proxy_scheme']
        # logger = Log().getLogger('development')
        # logger.info('parse error:{},time:{},level:{},item:{}'.format(failure, time.time(), self.level, item))
        yield item
        for i in range(QUEUE_NUM):
            length = self.conn.llen(QUEUE_KEY + str(i))
            if length:
                self.request = scrapy.Request(self.base_url, meta={'level':i}, priority = (QUEUE_NUM - i), callback=self.parse,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)
                yield self.request
        pass
        
        # logger = Log().getLogger('development')
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