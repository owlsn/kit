# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.item.ip66_item import Ip66Item
from ip_proxy.connection.redis_connection import RedisConnection
import time

class Ip66Spider(scrapy.Spider):
    name = 'ip66'
    base_url = 'http://www.66ip.cn'
    allowed_domains = ['www.66ip.cn']
    start_urls = ['http://www.66ip.cn/']

    def __init__(self):
        r = RedisConnection()
        self.conn = r.conn
        pass

    def parse(self, response):
        item = Ip66Item()
        for a in response.xpath('//div[@id="PageList"]/a'):
            value = a.xpath('@href').extract()
            if value and value[0].startswith('/', 0, 1):
                url = self.base_url + value[0]
                if not self.conn.get(url):
                    self.conn.set(url, 1)
                    yield self.make_requests_from_url(url)

        for li in response.xpath('//ul[@class="textlarge22"]/li'):
            value = li.xpath('a/@href').extract()
            if value and value[0].startswith('/', 0, 1):
                url = self.base_url + value[0]
                if not self.conn.get(url):
                    self.conn.set(url, 1)
                    yield self.make_requests_from_url(url)

        for tr in response.xpath('//table[@width="100%"]/tr'):
            td = tr.xpath('td/text()').extract()
            ip = td[0]
            port = td[1]
            if ip and ip != 'ip':
                item['ip'] = ip
                item['port'] = port
                yield item
