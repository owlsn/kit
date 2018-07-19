# coding = utf-8
from tornado.web import UIModule

class HeaderModule(UIModule):
    def render(self, show_header = 1):
        return self.render_string('common/header.html') if show_header else ''