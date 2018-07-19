from display.handlers.base import BaseHandler

class Examples404Handler(BaseHandler):
    def get(self):
        title = 'Examples404Handler'
        self.render('examples/404.html', title = title, **self.render_dict)