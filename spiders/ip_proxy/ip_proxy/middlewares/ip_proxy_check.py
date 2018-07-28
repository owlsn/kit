# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from ip_proxy.utils.log import Log
from ip_proxy.connection.redis_connection import redisDb1
from ip_proxy.connection.mysql_connection import mysqlAsyn
import socket
import struct
import time
import traceback
from ip_proxy.config import QUEUE_KEY
from scrapy.exceptions import IgnoreRequest
from ip_proxy.utils.ip_tools import IpTools

class IpProxyCheckBeginMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.conn = redisDb1.conn
        self.mysql = mysqlAsyn.dbpool
        pass

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        level = request.meta.get('level')
        if level is None:
            raise IgnoreRequest
        key = QUEUE_KEY + str(level)
        length = self.conn.llen(key)
        if not length:
            raise IgnoreRequest
        byte = self.conn.lpop(key)
        d_str = str(byte, encoding = "utf-8")  
        data = eval(d_str)
        if not data['ip'] or not data['port']:
            raise IgnoreRequest
        # 获取ip地址信息
        if 'flag' not in data.keys() or not data['flag']:
            info = {'ip' : data['ip'], 'key' : data['key']}
            res = self.mysql.runInteraction(self.do_update, info)
            res.addErrback(self.handle_error)

        scheme = data['scheme'] if data['scheme'] is not None else 'http'
        ip = socket.inet_ntoa(struct.pack('I',socket.htonl(int(data['ip']))))
        port = data['port']
        times = data['times'] if 'times' in data.keys() and data['times'] is not None else 0
        proxy = scheme + '://' + ip + ':' + str(port)
        request.meta['proxy'] = proxy
        request.meta['times'] = times
        request.meta['begin'] = time.time() * 1000
        request.meta['proxy_ip'] = data['ip']
        request.meta['proxy_port'] = data['port']
        request.meta['proxy_scheme'] = data['scheme']
        request.meta['key'] = data['key']
        # logger = Log().getLogger('development')
        # logger.info('begin middleware start, request.meta:{},time:{}'.format(request.meta, time.time()))
        return None
    
    def do_update(self, cursor, info):
        try:
            if ('ip' not in info.keys() or not info['ip']) or ('key' not in info.keys() or not info['key']):
                return
            else:
                tool = IpTools()
                ip = info['ip']
                key = info['key']
                r = tool.info(socket.inet_ntoa(struct.pack('I',socket.htonl(int(ip)))))
                if r != None and r['code'] == 0:
                    data = r['data']
                    isp = data['isp']
                    country =data['country']
                    city = data['city']
                    region = data['region']
                    area = data['area']
                    update_sql =  """ update ip set isp = %s,country = %s,region = %s, city = %s, area = %s, flag = 1 where id = %s;"""
                    params = (isp, country, region, city, area, key)
                    cursor.execute(update_sql, params)
                else:
                    return
            pass
        except:
            logger = Log().getLogger('development')
            logger.error(traceback.format_exc())
            pass

    def handle_error(self, failure):
        logger = Log().getLogger('development')
        logger.error(str(failure))
        pass

    def spider_opened(self, spider):
        pass

class IpProxyCheckEndMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_response(self, request, response, spider):
        if response.status == 200:
            delay = time.time() * 1000 - int(request.meta['begin'])
            request.meta['delay'] = delay
            # logger = Log().getLogger('development')
            # logger.info('end middleware start, request.meta:{},response:{},time:{}'.format(request.meta, response.request_meta, time.time()))
            return response
        else:
            raise IgnoreRequest
            pass

    def spider_opened(self, spider):
        pass

