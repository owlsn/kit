# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.item.ip66_item import Ip66Item
class Ip66Spider(scrapy.Spider):
    name = 'ip66'
    allowed_domains = ['www.66ip.cn']
    start_urls = ['http://www.66ip.cn/']

    def parse(self, response):
        item = Ip66Item()
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            #f.write(response.xpath('//p'))
            for tr in response.xpath('//p'):
                print(tr.xpath('text()').extract_first())
                f.write(tr.xpath('text()').extract_firs())
            #    f.write(tr.extract())
        pass
