# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.item.ip_item import IpItem
from ip_proxy.utils.log import Log
import time
import json
from ip_proxy.spiders.base import BaseSpider

class Ip66Spider(BaseSpider):
    name = 'ip66'
    base_url = 'http://www.66ip.cn/'
    allowed_domains = ['www.66ip.cn']
    start_urls = ['http://www.66ip.cn/']

    def parse(self, response):
        # logger = Log().getLogger('development')
        if response.url == self.base_url:
            # 解析起始页面的头部标签的url
            for li in response.xpath('//ul[@class="textlarge22"]/li'):
                value = li.xpath('a/@href').extract()
                if value and value[0].startswith('/', 0, 1):
                    url = self.base_url + value[0]
                    if not self.conn.get(url):
                        self.conn.set(url, 1, ex = 2 * 60 * 60)
                        yield self.make_requests_from_url(url)
        item = IpItem()
        # 解析分页的url
        for a in response.xpath('//div[@id="PageList"]/a'):
            value = a.xpath('@href').extract()
            if value and value[0].startswith('/', 0, 1):
                url = self.base_url + value[0]
                if not self.conn.get(url):
                    self.conn.set(url, 1, ex = 2 * 60 * 60)
                    yield self.make_requests_from_url(url)

        # 解析表格,获取ip数据
        for tr in response.xpath('//table[@width="100%"]/tr'):
            td = tr.xpath('td/text()').extract()
            ip = td[0]
            port = td[1]
            source = self.base_url
            if ip and ip != 'ip':
                item['ip'] = ip
                item['port'] = port
                item['source'] = source
                yield item
