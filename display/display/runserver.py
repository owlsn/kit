# coding = utf-8
from tornado import ioloop, web, options, httpserver, template, gen, httpclient
from routers import routers
import os, sys
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)
from display.config import *
from display.connections.mysql_connection import mysql
from display.connections.redis_connection import redisDb1
from display.utils.log import Log
import socket
import struct
import json
import re
import requests

from tornado.options import define, options
define('port', default = 8888, help = 'run on the given port', type = int)

class IndexHandler(web.RequestHandler):
    def get(self):
        title = 'index'
        self.render('index/index.html', title = title)

# class TestHandler(web.RequestHandler):
#     @web.asynchronous
#     @gen.engine
#     def get(self):
#         title = 'list'
#         self.render('index/data.html', title = title)

#     def post(self):
#         key = 'ip_queue_0'
#         d = self.application.redis.lpop(key)
#         logger = Log().getLogger('development')
#         logger.info(d)
#         db = self.application.conn
#         cursor = db.cursor()
#         sql = """select ip, port, scheme, level, flag, times, create_time, update_time  from `ip` order by update_time asc limit %s,%s """
#         params = (0, 10)
#         cursor.execute(sql, params)
#         res = cursor.fetchall()

#         client = httpclient.AsyncHTTPClient()
#         li = []
#         if res:
#             for value in res:
#                 ip = socket.inet_ntoa(struct.pack('I',socket.htonl(int(value[0]))))
#                 data = {'ip' : ip, 'port' : value[1], 'scheme' : value[2], 'level' : value[3], 'flag':value[4], 'times' : value[5], 'create_time': value[6], 'update_time' : value[7]}
#                 response = yield gen.Task(client.fetch, "http://ip.taobao.com/service/getIpInfo.php?ip=" + ip)
#                 info = json.loads(response.body.decode('utf-8'))
#                 if info['code'] == 0:       
#                     data['isp'] = info['data']['isp']
#                     data['city'] = info['data']['city']
#                     data['area'] = info['data']['area']
#                     data['region'] = info['data']['region']
#                     data['country'] = info['data']['country']
#                 li.append(data)
#         return json.dumps(li)

class ListHandler(web.RequestHandler):
    def get(self):
        title = 'list'
        self.render('index/data.html', title = title)

    def post(self):
        page = self.get_argument('page', 1)
        limit = self.get_argument('limit', 10)
        start = self.get_argument('start', 0)

        db = self.application.conn
        cursor = db.cursor()
        sql = """select ip, port, scheme, level, flag, times, create_time, update_time  from `ip` order by update_time asc limit %s,%s """
        params = (int(start), int(limit))
        count_sql = """select count(*) as count  from `ip` """
        cursor.execute(sql, params)
        res = cursor.fetchall()

        r = cursor.execute(count_sql)
        result = cursor.fetchone()
        total = result[0]
        li = []
        if res:
            for value in res:
                ip = socket.inet_ntoa(struct.pack('I',socket.htonl(int(value[0]))))
                data = {'ip' : ip, 'port' : value[1], 'scheme' : value[2], 'level' : value[3], 'flag':value[4], 'times' : value[5], 'create_time': value[6], 'update_time' : value[7]}
                li.append(data)
        data = {
            'page' : page,
            'start' : start,
            'limit' : limit,
            'data' : li,
            'total' : total
        }
        self.write(json.dumps(data))


class App(web.Application):
    def __init__(self):
        handers = [
            (r'/', IndexHandler),
            (r'/list', ListHandler)
        ]
        settings = dict(
            template_path = TEMPLATES,
            static_path = STATIC,
            debug = True
        )
        ui_modules = {
            'aside' : AsideModule,
            'header' : HeaderModule,
            'footer' : FooterModule
        }
        self.conn = mysql.get_instance().conn
        self.redis = redisDb1.conn
        web.Application.__init__(self, handers, ui_modules = ui_modules, **settings)

class AsideModule(web.UIModule):
    def render(self):
        return self.render_string('common/aside.html')

    # def css_files(self):
    #     return 'css/index.css'

    # def javascript_files(self):
    #     return 'js/index.js'

class HeaderModule(web.UIModule):
    def render(self):
        return self.render_string('common/header.html')

class FooterModule(web.UIModule):
    def render(self):
        return self.render_string('common/footer.html')


if __name__ == "__main__":
    options.parse_command_line()
    http_server = httpserver.HTTPServer(App())
    http_server.listen(options.port)
    ioloop.IOLoop.current().start()

# if __name__ == "__main__":
#     path = ROOT + '/public/static/dist/css/googleapis.fonts.css'
#     with open(path, 'r') as f:
#         regex = r'https:\/\/fonts.gstatic.com\/s\/sourcesanspro\/v11\/[\s\S]*?.woff2'
#         l = re.findall(regex, f.read())
#         length = len(l)
#         if length:
#             for value in l:
#                 name = value.split('/')
#                 path = ROOT + '/public/static/dist/fonts/' + name[-1]
#                 response = requests.get(value)
#                 if response.status_code == 200:
#                     with open(path, 'wb') as n:
#                         n.write(response.content)