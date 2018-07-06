# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.utils.log import log
import requests
from ip_proxy.spiders.base import BaseSpider
from ip_proxy.utils.image import img, Img
from ip_proxy.item.ip_item import IpItem

class CooboboSpider(BaseSpider):
    name = 'coobobo'
    allowed_domains = ['www.coobobo.com']
    base_url = 'http://www.coobobo.com/'
    start_urls = ['http://www.coobobo.com/free-http-proxy']

    def parse(self, response):
        logger = log.getLogger('development')
        item = IpItem()
        # 解析表格,获取ip数据
        img = Img(cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe')
        tr_list = response.xpath('//tbody/tr')
        if len(tr_list):
            for tr in tr_list:
                ip_tr = tr.xpath('td[1]/script/text()').extract()
                ip_str = ip_tr[0].strip() if ip_tr else None
                if ip_str:
                    s = ip_str[(ip_str.index('(') + 1):ip_str.index(')')]
                    ip = ''.join(map(lambda s:s.strip().strip('"').strip('\''), s.split('+')))
                    port_tr = tr.xpath('td[2]/img/@src').extract()
                    image_url = (self.base_url + port_tr[0]) if port_tr else None
                    if image_url:
                        header = {
                            'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
                        }
                        res = requests.get(image_url, headers = header)
                        # text = img.parse(res.content)
                        # print(text)

            for a in response.xpath('//ul[@class="pagination"]/li/a'):
                value = a.xpath('@href').extract()
                if value and value[0].startswith('/', 0, 1):
                    url = self.base_url + value[0].lstrip('/')
                    print(url)
                    # if not self.conn.get(url):
                    #     self.conn.set(url, 1, ex = 2 * 60 * 60)
                    #     yield self.make_requests_from_url(url)

        pass
