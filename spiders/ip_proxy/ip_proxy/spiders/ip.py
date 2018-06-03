# -*- coding: utf-8 -*-
import scrapy


class IpSpider(scrapy.Spider):
    name = 'ip'
    allowed_domains = ['www.ip163.com']
    start_urls = ['http://www.ip163.com/']

    def parse(self, response):
        pass
