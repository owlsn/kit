from display.handlers.base import BaseHandler

class LayoutNavHandler(BaseHandler):
    def get(self):
        title = 'LayoutNavHandler'
        self.render_dict['show_aside'] = 0
        self.render('layout/top-nav.html', title = title, **self.render_dict)