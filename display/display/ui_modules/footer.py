# coding = utf-8
from tornado.web import UIModule

class FooterModule(UIModule):
    def render(self, show_footer = 1):
        return self.render_string('common/footer.html') if show_footer else ''
