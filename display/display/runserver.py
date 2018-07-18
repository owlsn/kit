# coding = utf-8
from tornado import ioloop, web, options, httpserver, template, gen, httpclient, routing
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

class BaseHandler(web.RequestHandler):
    def initialize(self):
        show_header = 1
        show_aside = 1
        show_footer = 1
        self.render_dict = {'show_header' : show_header, 'show_aside' : show_aside, 'show_footer' : show_footer, 'uri' : self.request.uri}


class IndexHandler(BaseHandler):
    def get(self):
        index = self.get_argument('type', 1)
        title = 'IndexHandler'
        if index == 1:
            self.render('index/index1.html', title = title, **self.render_dict)
        else:
            self.render('index/index2.html', title = title, **self.render_dict)

# class TestHandler(BaseHandler):
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

class CalendarHandler(BaseHandler):
    def get(self):
        title = 'CalendarHandler'
        self.render('calendar/calendar.html', title = title, **self.render_dict)

class ChartsJsHandler(BaseHandler):
    def get(self):
        title = 'ChartsJsHandler'
        self.render('charts/chartjs.html', title = title, **self.render_dict)

class ChartsFlotHander(BaseHandler):
    def get(self):
        title = 'ChartsFlotHander'
        self.render('charts/flot.html', title = title, **self.render_dict)

class ChartsInlineHander(BaseHandler):
    def get(self):
        title = 'ChartsInlineHander'
        self.render('charts/inline.html', title = title, **self.render_dict)

class ChartsMorrisHander(BaseHandler):
    def get(self):
        title = 'ChartsMorrisHander'
        self.render('charts/morris.html', title = title, **self.render_dict)

class TablesDataHandler(BaseHandler):
    def get(self):
        title = 'TablesDataHandler'
        self.render('tables/data.html', title = title, **self.render_dict)

class Examples404Handler(BaseHandler):
    def get(self):
        title = 'Examples404Handler'
        self.render('examples/404.html', title = title, **self.render_dict)

class Examples500Handler(BaseHandler):
    def get(self):
        title = 'Examples500Handler'
        self.render('examples/500.html', title = title, **self.render_dict)

class ExamplesBlankHandler(BaseHandler):
    def get(self):
        title = 'ExamplesBlankHandler'
        self.render('examples/blank.html', title = title, **self.render_dict)

class ExamplesInvoiceHandler(BaseHandler):
    def get(self):
        title = 'ExamplesInvoiceHandler'
        self.render('examples/invoice.html', title = title, **self.render_dict)

class ExamplesPrintHandler(BaseHandler):
    def get(self):
        title = 'ExamplesPrintHandler'
        self.render_dict = {'show_header' : 0, 'show_aside' : 0, 'show_footer' : 0}
        self.render('examples/invoice-print.html', title = title, **self.render_dict)

class ExamplesLockScreenHandler(BaseHandler):
    def get(self):
        title = 'ExamplesLockScreenHandler'
        self.render_dict = {'show_header' : 0, 'show_aside' : 0, 'show_footer' : 0}
        self.render('examples/lockscreen.html', title = title, **self.render_dict)

class ExamplesLoginHandler(BaseHandler):
    def get(self):
        title = 'ExamplesLoginHandler'
        self.render_dict = {'show_header' : 0, 'show_aside' : 0, 'show_footer' : 0}
        self.render('examples/login.html', title = title, **self.render_dict)

class ExamplesPaceHandler(BaseHandler):
    def get(self):
        title = 'ExamplesPaceHandler'
        self.render('examples/pace.html', title = title, **self.render_dict)

class ExamplesProfileHandler(BaseHandler):
    def get(self):
        title = 'ExamplesProfileHandler'
        self.render('examples/profile.html', title = title, **self.render_dict)

class ExamplesRegisterHandler(BaseHandler):
    def get(self):
        title = 'ExamplesRegisterHandler'
        self.render_dict = {'show_header' : 0, 'show_aside' : 0, 'show_footer' : 0}
        self.render('examples/register.html', title = title, **self.render_dict)

class FormsAdvancedHandler(BaseHandler):
    def get(self):
        title = 'FormsAdvancedHandler'
        self.render('forms/advanced.html', title = title, **self.render_dict)

class FormsEditorsHandler(BaseHandler):
    def get(self):
        title = 'FormsEditorsHandler'
        self.render('forms/editors.html', title = title, **self.render_dict)

class FormsGeneralHandler(BaseHandler):
    def get(self):
        title = 'FormsGeneralHandler'
        self.render('forms/general.html', title = title, **self.render_dict)

class LayoutBoxedHandler(BaseHandler):
    def get(self):
        title = 'LayoutBoxedHandler'
        self.render('layout/boxed.html', title = title, **self.render_dict)

class LayoutSidebarHandler(BaseHandler):
    def get(self):
        title = 'LayoutSidebarHandler'
        self.render('layout/collapsed-sidebar.html', title = title, **self.render_dict)

class LayoutFixedHandler(BaseHandler):
    def get(self):
        title = 'LayoutFixedHandler'
        self.render('layout/fixed.html', title = title, **self.render_dict)

class LayoutNavHandler(BaseHandler):
    def get(self):
        title = 'LayoutNavHandler'
        self.render_dict['show_aside'] = 0
        self.render('layout/top-nav.html', title = title, **self.render_dict)

class MailboxComposeHandler(BaseHandler):
    def get(self):
        title = 'MailboxComposeHandler'
        self.render('mailbox/compose.html', title = title, **self.render_dict)

class MailboxHandler(BaseHandler):
    def get(self):
        title = 'MailboxHandler'
        self.render('mailbox/mailbox.html', title = title, **self.render_dict)

class MailboxReadHandler(BaseHandler):
    def get(self):
        title = 'MailboxReadHandler'
        self.render('mailbox/read-mail.html', title = title, **self.render_dict)

class TablesDataHandler(BaseHandler):
    def get(self):
        title = 'TablesDataHandler'
        self.render('tables/data.html', title = title, **self.render_dict)

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

class TablesSimpleHandler(BaseHandler):
    def get(self):
        title = 'TablesSimpleHandler'
        self.render('tables/simple.html', title = title, **self.render_dict)

class UiButtonsHandler(BaseHandler):
    def get(self):
        title = 'UiButtonsHandler'
        self.render('ui/buttons.html', title = title, **self.render_dict)

class UiGeneralHandler(BaseHandler):
    def get(self):
        title = 'UiGeneralHandler'
        self.render('ui/general.html', title = title, **self.render_dict)

class UiIconsHandler(BaseHandler):
    def get(self):
        title = 'UiIconsHandler'
        self.render('ui/icons.html', title = title, **self.render_dict)

class UiModalsHandler(BaseHandler):
    def get(self):
        title = 'UiModalsHandler'
        self.render('ui/modals.html', title = title, **self.render_dict)

class UiSlidersHandler(BaseHandler):
    def get(self):
        title = 'UiSlidersHandler'
        self.render('ui/sliders.html', title = title, **self.render_dict)

class UiTimelineHandler(BaseHandler):
    def get(self):
        title = 'UiTimelineHandler'
        self.render('ui/timeline.html', title = title, **self.render_dict)

class WidgetsHandler(BaseHandler):
    def get(self):
        title = 'WidgetsHandler'
        self.render('widgets/widgets.html', title = title, **self.render_dict)


class App(web.Application):
    def __init__(self):
        handers = [
            routing.URLSpec(r'/index', IndexHandler, name = 'index'),
            routing.URLSpec(r'/calendar', CalendarHandler, name = 'calendar'),
            routing.URLSpec(r'/charts/chartjs', ChartsJsHandler, name = 'chartjs'),
            routing.URLSpec(r'/charts/flot', ChartsFlotHander, name = 'flot'),
            routing.URLSpec(r'/charts/inline', ChartsInlineHander, name = 'inline'),
            routing.URLSpec(r'/charts/morris', ChartsMorrisHander, name = 'morris'),
            routing.URLSpec(r'/examples/404', Examples404Handler, name = '404'),
            routing.URLSpec(r'/examples/500', Examples500Handler, name = '500'),
            routing.URLSpec(r'/examples/blank', ExamplesBlankHandler, name = 'blank'),
            routing.URLSpec(r'/examples/invoice', ExamplesInvoiceHandler, name = 'invoice'),
            routing.URLSpec(r'/examples/print', ExamplesPrintHandler, name = 'print'),
            routing.URLSpec(r'/examples/lockscreen', ExamplesLockScreenHandler, name = 'lockscreen'),
            routing.URLSpec(r'/examples/login', ExamplesLoginHandler, name = 'login'),
            routing.URLSpec(r'/examples/pace', ExamplesPaceHandler, name = 'pace'),
            routing.URLSpec(r'/examples/profile', ExamplesProfileHandler, name = 'profile'),
            routing.URLSpec(r'/examples/register', ExamplesRegisterHandler, name = 'register'),
            routing.URLSpec(r'/forms/advanced', FormsAdvancedHandler, name = 'advanced'),
            routing.URLSpec(r'/forms/editors', FormsEditorsHandler, name = 'editors'),
            routing.URLSpec(r'/forms/general', FormsGeneralHandler, name = 'forms_general'),
            routing.URLSpec(r'/layout/boxed', LayoutBoxedHandler, name = 'boxed'),
            routing.URLSpec(r'/layout/sidebar', LayoutSidebarHandler, name = 'sidebar'),
            routing.URLSpec(r'/layout/fixed', LayoutFixedHandler, name = 'fixed'),
            routing.URLSpec(r'/layout/nav', LayoutNavHandler, name = 'nav'),
            routing.URLSpec(r'/mailbox/compose', MailboxComposeHandler, name = 'compose'),
            routing.URLSpec(r'/mailbox/mailbox', MailboxHandler, name = 'mailbox'),
            routing.URLSpec(r'/mailbox/read', MailboxReadHandler, name = 'read'),
            routing.URLSpec(r'/tables/data', TablesDataHandler, name = 'data'),
            routing.URLSpec(r'/tables/simple', TablesSimpleHandler, name = 'simple'),
            routing.URLSpec(r'/ui/buttons', UiButtonsHandler, name = 'buttons'),
            routing.URLSpec(r'/ui/general', UiGeneralHandler, name = 'ui_general'),
            routing.URLSpec(r'/ui/icons', UiIconsHandler, name = 'icons'),
            routing.URLSpec(r'/ui/modals', UiModalsHandler, name = 'modals'),
            routing.URLSpec(r'/ui/sliders', UiSlidersHandler, name = 'sliders'),
            routing.URLSpec(r'/ui/timeline', UiTimelineHandler, name = 'timeline'),
            routing.URLSpec(r'/widgets', WidgetsHandler, name = 'widgets'),
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
    def render(self, show_aside = 1):
        return self.render_string('common/aside.html') if show_aside else ''

    # def css_files(self):
    #     return 'css/index.css'

    # def javascript_files(self):
    #     return 'js/index.js'

class HeaderModule(web.UIModule):
    def render(self, show_header = 1):
        return self.render_string('common/header.html') if show_header else ''

class FooterModule(web.UIModule):
    def render(self, show_footer = 1):
        return self.render_string('common/footer.html') if show_footer else ''


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