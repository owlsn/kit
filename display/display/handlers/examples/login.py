from display.handlers.base import BaseHandler

class ExamplesLoginHandler(BaseHandler):
    def get(self):
        title = 'ExamplesLoginHandler'
        self.render_dict = {'show_header' : 0, 'show_aside' : 0, 'show_footer' : 0}
        self.render('examples/login.html', title = title, **self.render_dict)