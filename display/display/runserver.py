# coding = utf-8
from tornado import ioloop, web, options, httpserver, template
from routers import routers
import os, sys
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)
from display.config import *
from display.connections.mysql_connection import mysql

from tornado.options import define, options
define('port', default = 8888, help = 'run on the given port', type = int)

class IndexHandler(web.RequestHandler):
    def get(self):
        db = self.application.conn
        cursor = db.cursor()
        sql = """select ip, port, scheme, level, flag, times, create_time, update_time  from `ip` order by update_time asc limit %s,%s """
        params = (0, 10)
        cursor.execute(sql, params)
        res = cursor.fetchall()
        li = []
        if res:
            for value in res:
                data = {'ip' : value[0], 'port' : value[1], 'scheme' : value[2], 'level' : value[3], 'flag':value[4], 'times' : value[5], 'create_time': value[6], 'update_time' : value[7]}
                li.append(data)
        title = 'ip list'
        items = li
        self.render('index/index.html', title = title, items = items)

class App(web.Application):
    def __init__(self):
        handers = [
            (r'/', IndexHandler)
        ]
        settings = dict(
            template_path = TEMPLATES,
            static_path = STATIC,
            debug = True
        )
        ui_modules = {
            'ip' : IpModule
        }
        self.conn = mysql.get_instance().conn
        web.Application.__init__(self, handers, ui_modules = ui_modules, **settings)

class IpModule(web.UIModule):
    def render(self, item):
        return self.render_string('index/ip.html', item = item)

    def css_files(self):
        return 'css/index.css'

    def javascript_files(self):
        return 'js/index.js'


if __name__ == "__main__":
    options.parse_command_line()
    http_server = httpserver.HTTPServer(App())
    http_server.listen(options.port)
    ioloop.IOLoop.current().start()