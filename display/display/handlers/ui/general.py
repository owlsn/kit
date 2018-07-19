from display.handlers.base import BaseHandler

class UiGeneralHandler(BaseHandler):
    def get(self):
        title = 'UiGeneralHandler'
        self.render('ui/general.html', title = title, **self.render_dict)