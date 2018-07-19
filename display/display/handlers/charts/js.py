from display.handlers.base import BaseHandler

class ChartsJsHandler(BaseHandler):
    def get(self):
        title = 'ChartsJsHandler'
        self.render('charts/chartjs.html', title = title, **self.render_dict)