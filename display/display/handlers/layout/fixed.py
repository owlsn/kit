from display.handlers.base import BaseHandler

class LayoutFixedHandler(BaseHandler):
    def get(self):
        title = 'LayoutFixedHandler'
        self.render('layout/fixed.html', title = title, **self.render_dict)