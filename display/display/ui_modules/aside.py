# coding = utf-8
from tornado.web import UIModule

class AsideModule(UIModule):
    def render(self, show_aside = 1):
        return self.render_string('common/aside.html') if show_aside else ''

    # def css_files(self):
    #     return 'css/index.css'

    # def javascript_files(self):
    #     return 'js/index.js'