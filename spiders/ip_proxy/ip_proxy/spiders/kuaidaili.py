# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.item.ip_item import IpItem
from ip_proxy.utils.log import log
import time
import json
from ip_proxy.spiders.base import BaseSpider

class KuaidailiSpider(BaseSpider):
    name = 'kuaidaili'
    base_url = 'https://www.kuaidaili.com/'
    allowed_domains = ['www.kuaidaili.com']
    start_urls = [
        'https://www.kuaidaili.com/free/inha/',
        'https://www.kuaidaili.com/free/intr/'
        ]

    def parse(self, response):
        logger = log.getLogger('development')
        item = IpItem()
        # 解析分页的url
        for a in response.xpath('//div[@id="listnav"]/ul/li/a'):
            value = a.xpath('@href').extract()
            if value and value[0].startswith('/', 0, 1):
                url = self.base_url + value[0]
                if not self.conn.get(url):
                    self.conn.set(url, 1, ex = 2 * 60 * 60)
                    yield self.make_requests_from_url(url)

        # 解析表格,获取ip数据
        for tr in response.xpath('//div[@id="list"]/table/tbody/tr'):
            td = tr.xpath('td/text()').extract()
            ip = td[0]
            port = td[1]
            scheme = td[3]
            source = self.base_url
            if ip:
                item['ip'] = ip
                item['port'] = port
                item['scheme'] = scheme.lower()
                item['source'] = source
                yield item

        pass
