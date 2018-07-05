# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.utils.log import log
import time
import json
import re
import hashlib
import requests
from ip_proxy.spiders.base import BaseSpider
from ip_proxy.utils.image import img, Img

class CooboboSpider(BaseSpider):
    name = 'coobobo'
    allowed_domains = ['www.coobobo.com']
    base_url = 'http://www.coobobo.com/'
    start_urls = ['http://www.coobobo.com/free-http-proxy']

    def parse(self, response):
        logger = log.getLogger('development')
        item = IpItem()
        # 解析表格,获取ip数据
        # img = Img(cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe')
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
                        'Cookie': proxy_token,
                        'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5'
                    }
                    res = requests.get(image_url, headers = header)
                    if res.status_code == 200:
                        text = img.parse(res.content)
                        logger.info(text)
        pass
