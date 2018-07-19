from display.handlers.base import BaseHandler

class UiSlidersHandler(BaseHandler):
    def get(self):
        title = 'UiSlidersHandler'
        self.render('ui/sliders.html', title = title, **self.render_dict)