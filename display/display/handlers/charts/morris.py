from display.handlers.base import BaseHandler

class ChartsMorrisHander(BaseHandler):
    def get(self):
        title = 'ChartsMorrisHander'
        self.render('charts/morris.html', title = title, **self.render_dict)