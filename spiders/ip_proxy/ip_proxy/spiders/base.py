# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from ip_proxy.connection.redis_connection import RedisConnection
from ip_proxy.config import SPIDER_SET

class BaseSpider(scrapy.Spider):

    def __init__(self):
        # redis连接,主要用于url判重
        r = RedisConnection(db = 2)
        self.conn = r.conn
        self.spider_set = SPIDER_SET if SPIDER_SET else 'spider_set'
        pass

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider
        pass
    
    def spider_closed(self, spider, reason):
        cls_name = self.__class__.__name__
        self.conn.srem(self.spider_set, cls_name)
        pass

    def spider_opened(self, spider):
        cls_name = self.__class__.__name__
        self.conn.sadd(self.spider_set, cls_name)
        pass