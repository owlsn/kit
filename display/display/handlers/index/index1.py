from display.handlers.base import BaseHandler

class Index1Handler(BaseHandler):
    def get(self):
        title = 'Index1Handler'
        self.render('index/index1.html', title = title, **self.render_dict)