from display.handlers.base import BaseHandler

class ExamplesPrintHandler(BaseHandler):
    def get(self):
        title = 'ExamplesPrintHandler'
        self.render_dict = {'show_header' : 0, 'show_aside' : 0, 'show_footer' : 0}
        self.render('examples/invoice-print.html', title = title, **self.render_dict)