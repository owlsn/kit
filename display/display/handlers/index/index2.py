from display.handlers.base import BaseHandler

class Index2Handler(BaseHandler):
    def get(self):
        title = 'Index2Handler'
        self.render('index/index2.html', title = title, **self.render_dict)