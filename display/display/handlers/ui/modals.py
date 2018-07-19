from display.handlers.base import BaseHandler

class UiModalsHandler(BaseHandler):
    def get(self):
        title = 'UiModalsHandler'
        self.render('ui/modals.html', title = title, **self.render_dict)