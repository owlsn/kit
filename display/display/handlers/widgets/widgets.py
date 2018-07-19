from display.handlers.base import BaseHandler

class WidgetsHandler(BaseHandler):
    def get(self):
        title = 'WidgetsHandler'
        self.render('widgets/widgets.html', title = title, **self.render_dict)