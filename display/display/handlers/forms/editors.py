from display.handlers.base import BaseHandler

class FormsEditorsHandler(BaseHandler):
    def get(self):
        title = 'FormsEditorsHandler'
        self.render('forms/editors.html', title = title, **self.render_dict)