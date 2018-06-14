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
        item = CheckItem()
        item['ip'] = response.meta.get('ip')
        item['port']  = response.meta.get('port')
        item['delay']  = response.meta.get('delay')
        proxy = response.meta.get('proxy')
        url = response.url
        code = response.status
        if code == 200:
            logger = log.getLogger('debug')
            logger.debug('response-proxy:{},delay:{},url:{},code:{}'.format(proxy, item['delay'], url, code))
            yield item
        pass