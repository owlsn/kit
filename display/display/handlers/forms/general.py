from display.handlers.base import BaseHandler

class FormsGeneralHandler(BaseHandler):
    def get(self):
        title = 'FormsGeneralHandler'
        self.render('forms/general.html', title = title, **self.render_dict)