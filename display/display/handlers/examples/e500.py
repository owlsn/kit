from display.handlers.base import BaseHandler

class Examples500Handler(BaseHandler):
    def get(self):
        title = 'Examples500Handler'
        self.render('examples/500.html', title = title, **self.render_dict)