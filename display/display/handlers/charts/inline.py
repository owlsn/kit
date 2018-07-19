from display.handlers.base import BaseHandler

class ChartsInlineHander(BaseHandler):
    def get(self):
        title = 'ChartsInlineHander'
        self.render('charts/inline.html', title = title, **self.render_dict)