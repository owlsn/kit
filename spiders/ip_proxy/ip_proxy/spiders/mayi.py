# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.item.ip_item import IpItem
from ip_proxy.utils.log import log
import time
import json
import hashlib
import requests
from io import BytesIO
from ip_proxy.spiders.base import BaseSpider
from ip_proxy.config import IMAGE_PATH
from PIL import Image
import pytesseract

class MayiSpider(BaseSpider):
    name = 'mayi'
    base_url = 'http://www.mayidaili.com/'
    allowed_domains = ['www.mayidaili.com']
    start_urls = [
        'http://www.mayidaili.com/free',
        'http://www.mayidaili.com/share/'
        ]

    def parse(self, response):
        # logger = log.getLogger('development')
        item = IpItem()
        # 解析表格,获取ip数据
        tr_list = response.xpath('//tbody/tr')
        if len(tr_list):
            for tr in tr_list:
                ip_tr = tr.xpath('td[1]/text()').extract()
                ip = ip_tr[0].strip() if ip_tr else None
                image = tr.xpath('td[2]/img/@data-uri').extract()
                image_url = image[0].strip() if image else None
                source = self.base_url
                if image_url:
                    header = {
                        'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
                        'Referer' : 'http://www.mayidaili.com/free',
                        'Cookie': 'proxy_token=IklhMDPc; Hm_lvt_dad083bfc015b67e98395a37701615ca=1529815110; Hm_lpvt_dad083bfc015b67e98395a37701615ca=1529815110'
                    }
                    res = requests.get(image_url, headers = header)
                    print(res)
                    # text=pytesseract.image_to_string(Image.open(res.content))
                    # print(text)
                # if ip and image_url:
                #     item['ip'] = ip
                #     item['port'] = port
                #     item['source'] = source
                #     yield item

            # 解析分页的url
            for a in response.xpath('//ul[@class="pagination"]/li/a'):
                value = a.xpath('@href').extract()
                if value and value[0].startswith('http', 0, 4):
                    url = value[0]
                    print(url)
                    # if not self.conn.get(url):
                    #     self.conn.set(url, 1, ex = 2 * 60 * 60)
                    #     yield self.make_requests_from_url(url)

        pass
