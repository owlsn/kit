# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.item.ip_item import IpItem
from ip_proxy.utils.log import log
import time
import json
from ip_proxy.spiders.base import BaseSpider

class Ip89Spider(BaseSpider):
    name = 'ip89'
    base_url = 'http://www.89ip.cn/'
    allowed_domains = ['www.89ip.cn']
    start_urls = ['http://www.89ip.cn/']

    def parse(self, response):
        # logger = log.getLogger('development')
        item = IpItem()

        # 解析表格,获取ip数据
        tr_list = response.xpath('//table[@class="layui-table"]/tbody/tr')
        if len(tr_list):
            for tr in tr_list:
                td = tr.xpath('td/text()').extract()
                ip = td[0].strip()
                port = td[1].strip()
                source = self.base_url
                if ip and ip != 'ip':
                    item['ip'] = ip
                    item['port'] = port
                    item['source'] = source
                    yield item

            # 解析分页的url
            for a in response.xpath('//div[@id="layui-laypage-1"]/a'):
                value = a.xpath('@href').extract()
                if value and value[0].startswith('index', 0, 5):
                    url = self.base_url + value[0]
                    if not self.conn.get(url):
                        self.conn.set(url, 1, ex = 6 * 60 * 60)
                        yield self.make_requests_from_url(url)
