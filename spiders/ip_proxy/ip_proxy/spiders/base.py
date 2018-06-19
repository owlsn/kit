# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals

class BaseSpider(scrapy.Spider):

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider
        pass
    
    def spider_closed(self, spider, reason):
        pass

    def spider_opened(self, spider):
        pass