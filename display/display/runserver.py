# coding = utf-8
from tornado import ioloop, web, options, httpserver, template, gen, httpclient, routing
import os, sys
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)
from display.config import *
from display.connections.mysql_connection import mysql
from display.connections.redis_connection import redisDb1
from display.routers import ROUTERS, UI_MODULES

from tornado.options import define, options
define('port', default = 8888, help = 'run on the given port', type = int)

class App(web.Application):
    def __init__(self):
        handers = ROUTERS
        settings = dict(
            template_path = TEMPLATES,
            static_path = STATIC,
            debug = True
        )
        ui_modules = UI_MODULES
        self.conn = mysql.get_instance().conn
        self.redis = redisDb1.conn
        web.Application.__init__(self, handers, ui_modules = ui_modules, **settings)

if __name__ == "__main__":
    options.parse_command_line()
    http_server = httpserver.HTTPServer(App())
    http_server.listen(options.port)
    ioloop.IOLoop.current().start()