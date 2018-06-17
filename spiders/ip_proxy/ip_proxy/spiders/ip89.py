# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.item.ip_item import IpItem
from ip_proxy.connection.redis_connection import RedisConnection
from ip_proxy.utils.log import log
import time
import json

class Ip89Spider(scrapy.Spider):
    name = 'ip89'
    base_url = 'http://www.89ip.cn/'
    allowed_domains = ['www.89ip.cn']
    start_urls = ['http://www.89ip.cn/']

    def __init__(self):
        # redis连接,主要用于url判重
        r = RedisConnection()
        self.conn = r.conn
        pass

    def parse(self, response):
        logger = log.getLogger('development')
        item = IpItem()
        # 解析分页的url
        for a in response.xpath('//div[@id="layui-laypage-1"]/a'):
            value = a.xpath('@href').extract()
            if value and value[0].startswith('index', 0, 5):
                url = self.base_url + value[0]
                if not self.conn.get(url):
                    logger.info('url:{}is new'.format(url))
                    self.conn.set(url, 1)
                    yield self.make_requests_from_url(url)

        # 解析表格,获取ip数据
        for tr in response.xpath('//table[@class="layui-table"]/tbody/tr'):
            td = tr.xpath('td/text()').extract()
            ip = td[0].strip()
            port = td[1].strip()
            # print('ip:{},port:{}'.format(ip, port))
            if ip and ip != 'ip':
                item['ip'] = ip
                item['port'] = port
                yield item