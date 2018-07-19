from display.handlers.base import BaseHandler

class ExamplesBlankHandler(BaseHandler):
    def get(self):
        title = 'ExamplesBlankHandler'
        self.render('examples/blank.html', title = title, **self.render_dict)