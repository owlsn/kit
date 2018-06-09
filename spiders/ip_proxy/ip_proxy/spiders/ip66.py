# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.item.ip66_item import Ip66Item
from ip_proxy.connection.redis_connection import RedisConnection
import time
from ip_proxy.config import LOG_PATH
import json

class Ip66Spider(scrapy.Spider):
    name = 'ip66'
    base_url = 'http://www.66ip.cn/'
    allowed_domains = ['www.66ip.cn']
    start_urls = ['http://www.66ip.cn/']

    def __init__(self):
        # redis连接,主要用于url判重
        r = RedisConnection()
        self.conn = r.conn
        pass

    def parse(self, response):
        if response.url == self.base_url:
            # 解析起始页面的头部标签的url
            for li in response.xpath('//ul[@class="textlarge22"]/li'):
                value = li.xpath('a/@href').extract()
                if value and value[0].startswith('/', 0, 1):
                    url = self.base_url + value[0]
                    if not self.conn.get(url):
                        self.conn.set(url, 1)
                        yield self.make_requests_from_url(url)
        item = Ip66Item()
        # 解析分页的url
        for a in response.xpath('//div[@id="PageList"]/a'):
            value = a.xpath('@href').extract()
            if value and value[0].startswith('/', 0, 1):
                url = self.base_url + value[0]
                if not self.conn.get(url):
                    self.conn.set(url, 1)
                    yield self.make_requests_from_url(url)

        # 解析表格,获取ip数据
        for tr in response.xpath('//table[@width="100%"]/tr'):
            td = tr.xpath('td/text()').extract()
            ip = td[0]
            port = td[1]
            if ip and ip != 'ip':
                # with open(LOG_PATH + 'test.log', 'a') as f:
                #     f.write(ip + ':' + str(id(item)) + "\n")
                item['ip'] = ip
                item['port'] = port
                yield item
