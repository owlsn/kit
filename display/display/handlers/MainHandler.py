import tornado.ioloop
import tornado.web
import config

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Main Item 1", "Main Item 2", "Main Item 3"]
        self.render(config.template_path + "main/main.html", title="My title", items=items)