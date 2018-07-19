from display.handlers.base import BaseHandler

class ExamplesPaceHandler(BaseHandler):
    def get(self):
        title = 'ExamplesPaceHandler'
        self.render('examples/pace.html', title = title, **self.render_dict)