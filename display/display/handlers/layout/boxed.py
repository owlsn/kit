from display.handlers.base import BaseHandler

class LayoutBoxedHandler(BaseHandler):
    def get(self):
        title = 'LayoutBoxedHandler'
        self.render('layout/boxed.html', title = title, **self.render_dict)