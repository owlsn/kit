from display.handlers.base import BaseHandler

class FormsAdvancedHandler(BaseHandler):
    def get(self):
        title = 'FormsAdvancedHandler'
        self.render('forms/advanced.html', title = title, **self.render_dict)
