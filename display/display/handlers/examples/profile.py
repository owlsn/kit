from display.handlers.base import BaseHandler

class ExamplesProfileHandler(BaseHandler):
    def get(self):
        title = 'ExamplesProfileHandler'
        self.render('examples/profile.html', title = title, **self.render_dict)