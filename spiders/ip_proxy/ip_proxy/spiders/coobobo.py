# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.utils.log import Log
import requests
from ip_proxy.spiders.base import BaseSpider
from ip_proxy.utils.image import img, Img
from ip_proxy.item.ip_item import IpItem
from io import BytesIO
from PIL import Image
import hashlib

class CooboboSpider(BaseSpider):
    image_dict = {
        '02a28ea5ec13b64092fab59951ff6ea1' : 0,
        '5a56abdb2c50a5fe8afee52342f14575' : 8
    }
    name = 'coobobo'
    allowed_domains = ['www.coobobo.com']
    base_url = 'http://www.coobobo.com/'
    start_urls = ['http://www.coobobo.com/free-http-proxy']

    def parse(self, response):
        logger = Log().getLogger('development')
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
                    port = None
                    image_url = (self.base_url + port_tr[0]) if port_tr else None
                    if image_url:
                        header = {
                            'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
                        }
                        res = requests.get(image_url, headers = header)
                        if res.status_code == 200:
                            text = self.parse_port(BytesIO(res.content))
                            port = text if text else None
                    if ip and port:
                        item['ip'] = ip
                        item['port'] = port
                        item['source'] = source
                        yield item

            for a in response.xpath('//ul[@class="pagination"]/li/a'):
                value = a.xpath('@href').extract()
                if value and value[0].startswith('/', 0, 1):
                    url = self.base_url + value[0].lstrip('/')
                    if not self.conn.get(url):
                        self.conn.set(url, 1, ex = 2 * 60 * 60)
                        yield self.make_requests_from_url(url)

        pass

    def parse_port(self, content):
        image = Image.open(content)
        r, c = image.size
        image = image.crop((1, 3, (r - 1), (c - 4)))
        x, y = image.size
        num = int((x + 2) / 9)
        if num:
            result = ''
            for i in range(num):
                num_image = image.crop((i * 9, 0, (i + 1) * 9 - 2, 10))
                byte = num_image.tobytes()
                md5_obj = hashlib.md5(byte)
                md5_str = md5_obj.hexdigest()
                if md5_str and md5_str in self.image_dict.keys():
                    result += str(self.image_dict[md5_str])
                num_image.save('{}.gif'.format(md5_str))
        return result
