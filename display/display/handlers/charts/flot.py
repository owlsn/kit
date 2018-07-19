from display.handlers.base import BaseHandler

class ChartsFlotHander(BaseHandler):
    def get(self):
        title = 'ChartsFlotHander'
        self.render('charts/flot.html', title = title, **self.render_dict)