# -*- coding: utf-8 -*-
import scrapy
from app.items.fang import FangItem

class FangSpider(scrapy.Spider):
    name = "fang"
    allowed_domains = ["fang.com"]
    start_urls = ['http://wuhan.fang.com/']

    def parse(self, response):
        for li in response.xpath('//ul/li'):
            item = FangItem()
            item['link'] = li.xpath('a/@href').extract()
            yield item
