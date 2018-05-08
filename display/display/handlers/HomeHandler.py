import tornado.ioloop
import tornado.web
import config

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Home Item 1", "Home Item 2", "Home Item 3"]
        self.render(config.template_path + "home/home.html", title="My title", items=items)