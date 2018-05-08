import tornado.ioloop
import tornado.web
import sys
import config

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Index Item 1", "Index Item 2", "Index Item 3"]
        self.render(config.template_path + "index/index.html", title="My title", items=items)