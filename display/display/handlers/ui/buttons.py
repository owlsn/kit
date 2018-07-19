from display.handlers.base import BaseHandler

class UiButtonsHandler(BaseHandler):
    def get(self):
        title = 'UiButtonsHandler'
        self.render('ui/buttons.html', title = title, **self.render_dict)