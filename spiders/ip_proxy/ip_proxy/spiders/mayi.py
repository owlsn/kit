# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings
from ip_proxy.item.ip_item import IpItem
from ip_proxy.utils.log import log
import re
import requests
from ip_proxy.spiders.base import BaseSpider
from PIL import Image
from io import BytesIO

class MayiSpider(BaseSpider):
    name = 'mayi'
    base_url = 'http://www.mayidaili.com/'
    allowed_domains = ['www.mayidaili.com']
    start_urls = [
        'http://www.mayidaili.com/free'
        ]

    def parse(self, response):
        logger = log.getLogger('development')
        item = IpItem()
        # logger.info(response.text)
        regex = r'proxy_token=[\s\S]{8}'
        l = re.findall(regex, response.text)
        proxy_token = l[0] if l else None
        if not proxy_token:
            return
        # 解析表格,获取ip数据
        tr_list = response.xpath('//tbody/tr')
        if len(tr_list):
            for tr in tr_list:
                ip_tr = tr.xpath('td[1]/text()').extract()
                ip = ip_tr[0].strip() if ip_tr else None
                image = tr.xpath('td[2]/img/@data-uri').extract()
                image_url = image[0].strip() if image else None
                source = self.base_url
                port = None
                if image_url:
                    header = {
                        'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
                        'Referer' : 'http://www.mayidaili.com/free',
                        'Cookie': proxy_token,
                        'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5'
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

            # 解析分页的url
            for a in response.xpath('//ul[@class="pagination"]/li/a'):
                value = a.xpath('@href').extract()
                if value and value[0].startswith('http', 0, 4):
                    url = value[0]
                    if not self.conn.get(url):
                        self.conn.set(url, 1, ex = 2 * 60 * 60)
                        yield self.make_requests_from_url(url)
        pass

    def parse_port(self, content):
        # 去干扰线
        image = Image.open(content).crop((0, 6, 80, 15))
        image_array = image.load()
        x, y = image.size
        for i in range(x):
            for j in range(y):
                if image_array[i, j] != (0, 0, 0, 255):
                    image_array[i, j] = (0, 0, 0, 0)
        # 字符位置检测
        crop_position_array = []
        start_flag = False
        start_ci = 0
        for ci in range(x):
            check_col_result = self.check_col(image_array, ci, y)
            # print(check_col_result, ci)
            if start_flag and not check_col_result:
                crop_item = (start_ci, 0, ci, 9)
                crop_position_array.append(crop_item)
                start_flag = False
                start_ci = 0
            if not start_flag and check_col_result:
                start_flag = True
                start_ci = ci


        # 切割识别所有字符
        index = 0
        code_string = ''
        for cro_i in crop_position_array:
            co_result = self.recognition(image.crop(cro_i))
            if co_result:
                code_string += co_result
            else:
                return None
            index += 1
        return code_string
        pass

    # 边界检测
    def check_col(self, image_array_a, col, y_num):
        this_col = False
        for jj in range(y_num):
            if image_array_a[col, jj] != (0, 0, 0, 0):
                this_col = True
        return this_col

    def recognition(self, item_image):
        item_array = item_image.load()
        item_x, item_y = item_image.size
        settings = get_project_settings()
        path = settings['ROOT_PATH']
        for std_i in range(10):
            std_path = path + "/images/mayi/%d.png" % std_i
            std_item = Image.open(std_path)
            std_array = std_item.load()
            std_x, std_y = std_item.size
            this_flag = True
            if item_x == std_x and item_y == std_y:
                for f_x in range(item_x):
                    for f_y in range(item_y):
                        if item_array[f_x, f_y] != std_array[f_x, f_y]:
                            if this_flag:
                                this_flag = False
                if this_flag:
                    return str(std_i)
        return False