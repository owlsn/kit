# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.spiders.base import BaseSpider
from ip_proxy.item.ip_item import IpItem
from ip_proxy.utils.log import log

class Data5uSpider(BaseSpider):
    name = 'data5u'
    allowed_domains = ['www.data5u.com']
    base_url = 'http://www.data5u.com/'
    start_urls = [
        'http://www.data5u.com/free/index.html',
        'http://www.data5u.com/free/gngn/index.shtml',
        'http://www.data5u.com/free/gnpt/index.shtml',
        'http://www.data5u.com/free/gwgn/index.shtml',
        'http://www.data5u.com/free/gwpt/index.shtml'
    ]

    def parse(self, response):
        logger = log.getLogger('development')
        item = IpItem()
        # 解析表格,获取ip数据
        for ul in response.xpath('//div[@class="wlist"]/ul/li[2]/ul'):
            li = ul.xpath('span/li/text()').extract()
            ip = li[0]
            port = li[1]
            scheme = ul.xpath('span[4]/li/a/text()').extract()
            source = self.base_url
            if ip and ip != 'IP':
                item['ip'] = ip
                item['port'] = port
                item['source'] = source
                item['scheme'] = scheme[0].lower() if scheme else None
                yield item