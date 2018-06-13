# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.connection.redis_connection import RedisConnection
from ip_proxy.utils.log import log
from ip_proxy.item.check_item import CheckItem

class CheckSpider(scrapy.Spider):
    name = 'check'
    allowed_domains = ['www.66ip.cn']
    start_urls = ['http://www.66ip.cn/']

    custom_settings = {
        'RETRY_ENABLED': False,
        'HTTPPROXY_AUTH_ENCODING' : 'utf-8',
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
        item = CheckItem()
        proxy = response.meta.get('proxy')
        delay = response.meta.get('delay')
        url = response.url
        code = response.status
        logger = log.getLogger('debug')
        logger.debug('response-proxy:{},delay:{},url:{},code:{}'.format(proxy, delay, url, code))
        pass

    def parse_error(self, failure):
        request = failure.request
        proxy = request.meta.get('proxy')
        logger = log.getLogger('debug')
        logger.debug('proxy {} has been failed,{} is raised'.format(proxy, failure))
        # crawler_logger.error('proxy {} has failed, {} is raised'.format(proxy, failure))
        # print('proxy {} has been failed,{} is raised'.format(proxy, failure))
        # if failure.check(TimeoutError, TCPTimedOutError):
        #     decr = -1
        # else:
        #     decr = '-inf'

        # items = self.set_item_queue(request.url, proxy, self.init_score, decr)
        # for item in items:
        #     yield item
