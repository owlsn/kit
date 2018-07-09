# -*- coding: utf-8 -*-
import scrapy
from ip_proxy.utils.log import log
import requests
from ip_proxy.spiders.base import BaseSpider
from ip_proxy.utils.image import img, Img
from ip_proxy.item.ip_item import IpItem
from io import BytesIO
from PIL import Image

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
                    port = None
                    image_url = (self.base_url + port_tr[0]) if port_tr else None
                    if image_url:
                        header = {
                            'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
                        }
                        res = requests.get(image_url, headers = header)
                        if res.status_code == 200:
                            text = self.parse_port(BytesIO(res.content))
                            return
                            # port = text if text else None

            for a in response.xpath('//ul[@class="pagination"]/li/a'):
                value = a.xpath('@href').extract()
                if value and value[0].startswith('/', 0, 1):
                    url = self.base_url + value[0].lstrip('/')
                    print(url)
                    # if not self.conn.get(url):
                    #     self.conn.set(url, 1, ex = 2 * 60 * 60)
                    #     yield self.make_requests_from_url(url)

        pass

    def parse_port(self, content):
        # 去干扰线
        image = Image.open(content)
        r, c = image.size
        image = image.crop((1, 3, (r - 1), (c - 4)))
        x, y = image.size
        image_array = image.load()
        # image.save('test.gif')

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