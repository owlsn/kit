# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.item.ip66_item import Ip66Item
from ip_proxy.tool.ip_address import IpAddress
import time

class Ip66Spider(scrapy.Spider):
    name = 'ip66'
    allowed_domains = ['www.66ip.cn']
    start_urls = ['http://www.66ip.cn/']

    def parse(self, response):
        item = Ip66Item()
        item['ip_list'] = []
        filename = response.url.split("/")[-2] + '.html'
        for tr in response.xpath('//div[@class="container"]/div/div/table/tr'):
            ip = tr.xpath('td/text()').extract_first()
            if ip != 'ip':
                r = IpAddress.info(ip)
                time.sleep(1)
                if r != None and r['code'] == 0:
                    item['ip_list'].append(r['data'])
        yield item
