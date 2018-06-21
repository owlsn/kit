# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.item.ip_item import IpItem
from ip_proxy.utils.log import log
import time
import json
from ip_proxy.spiders.base import BaseSpider

class XiciSpider(BaseSpider):
    name = 'xici'
    base_url = 'http://www.xicidaili.com/'
    allowed_domains = ['www.xicidaili.com']
    start_urls = [
        'http://www.xicidaili.com/nn/',
        'http://www.xicidaili.com/nt/',
        'http://www.xicidaili.com/wn/',
        'http://www.xicidaili.com/wt/'
        ]

    def start_requests(self):
        # 对应level的url放入对应的队列，而url的leve是由delay确定
        for url in self.start_urls:
            yield scrapy.Request(url, headers = {'Referer': 'http://www.xicidaili.com/'})
        pass

    def parse(self, response):
        # logger = log.getLogger('development')
        item = IpItem()
        # 解析分页的url
        # for a in response.xpath('//div[@id="PageList"]/a'):
        #     value = a.xpath('@href').extract()
        #     if value and value[0].startswith('/', 0, 1):
        #         url = self.base_url + value[0]
        #         if not self.conn.get(url):
        #             self.conn.set(url, 1, ex = 6 * 60 * 60)
        #             yield self.make_requests_from_url(url)

        # 解析表格,获取ip数据
        for tr in response.xpath('//table[@id="ip_list"]/tr'):
            td = tr.xpath('td/text()').extract()
            ip = td[1].strip()
            port = td[2].strip()
            scheme = td[4].strip()
            source = self.base_url
            if ip:
                item['ip'] = ip
                item['port'] = port
                item['scheme'] = scheme
                item['source'] = source
                print(item)
                # yield item
        pass
