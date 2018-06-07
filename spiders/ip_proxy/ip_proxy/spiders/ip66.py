# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.item.ip66_item import Ip66Item
from ip_proxy.tool.ip_address import IpAddress
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
        for li in response.xpath('//ul[@class="textlarge22"]/li'):
            value = li.xpath('a/@href').extract()
            if value:
                url = self.base_url + value[0]
                if not self.conn.get(url):
                    yield self.make_requests_from_url(url)
                else:
                    self.conn.set(url, 1)
        return
        item = Ip66Item()
        for tr in response.xpath('//div[@class="container"]/div/div/table/tr'):
            ip = tr.xpath('td/text()').extract_first()
            if ip != 'ip':
                r = IpAddress.info(ip)
                if r != None and r['code'] == 0:
                    data = r['data']
                    item['ip'] = data['ip']
                    item['isp'] = data['isp']
                    item['country'] =data['country']
                    item['city'] = data['city']
                    item['region'] = data['region']
                    item['area'] = data['area']
                    item['create_time'] = time.time()
                    yield item
