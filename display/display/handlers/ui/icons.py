from display.handlers.base import BaseHandler

class UiIconsHandler(BaseHandler):
    def get(self):
        title = 'UiIconsHandler'
        self.render('ui/icons.html', title = title, **self.render_dict)
