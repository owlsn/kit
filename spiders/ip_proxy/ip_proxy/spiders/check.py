# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.connection.redis_connection import RedisConnection
from ip_proxy.utils.log import log
from ip_proxy.item.check_item import CheckItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
import time

class CheckSpider(scrapy.Spider):
    name = 'check'
    allowed_domains = ['www.66ip.cn']
    start_urls = ['http://www.66ip.cn/']

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)

    custom_settings = {
        'RETRY_ENABLED' : False,
        'RETRY_TIMES' : 2,
        'DOWNLOAD_TIMEOUT' : 30,
        'HTTPPROXY_AUTH_ENCODING' : 'utf-8',
        'CONCURRENT_REQUESTS' : 50,
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 50,
        'DOWNLOADER_MIDDLEWARES': {
            'ip_proxy.middlewares.random_user_agent.RandomUserAgentMiddleware' : 602,
            'ip_proxy.middlewares.ip_proxy_check.IpProxyCheckBeginMiddleware': 603,
            'ip_proxy.middlewares.ip_proxy_check.IpProxyCheckEndMiddleware': 601,
        },
        'ITEM_PIPELINES': {
            'ip_proxy.pipelines.check_pipeline.CheckPipeline': 200,
        },
        'LOG_LEVEL' : 'INFO',
        'LOG_PATH' : log.config['handlers']['error_file_handler']['filename']
    }

    def __init__(self):
        # redis连接,主要用于url判重
        r = RedisConnection()
        self.conn = r.conn
        pass

    def parse(self, response):
        logger = log.getLogger('debug')
        item = CheckItem()
        item['ip'] = response.meta.get('ip')
        item['port']  = response.meta.get('port')
        item['delay']  = response.meta.get('delay')
        proxy = response.meta.get('proxy')
        url = response.url
        code = response.status
        if code == 200:
            logger.debug('response-proxy:{},delay:{},url:{},code:{}'.format(proxy, item['delay'], url, code))
            yield item
        else:
            logger.debug('code:{}'.format(code))
        pass
    
    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        logger = log.getLogger('debug')
        logger.info('error:{}'.format(int(time.time() * 1000)))
        logger = log.getLogger('debug')
        self.logger.error(repr(failure))

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            logger.info('HttpError on {}'.format(response.url))
            self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            logger.info('DNSLookupError on {}'.format(response.url))
            self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            logger.info('TimeoutError on {}'.format(request.url))
            self.logger.error('TimeoutError on %s', request.url)