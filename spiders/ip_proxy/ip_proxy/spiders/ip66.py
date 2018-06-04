# -*- coding: utf-8 -*-
import scrapy


class Ip66Spider(scrapy.Spider):
    name = 'ip66'
    allowed_domains = ['www.66ip.cn']
    start_urls = ['http://www.66ip.cn/']

    def parse(self, response):
        pass
