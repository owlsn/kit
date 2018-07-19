from display.handlers.base import BaseHandler

class TablesSimpleHandler(BaseHandler):
    def get(self):
        title = 'TablesSimpleHandler'
        self.render('tables/simple.html', title = title, **self.render_dict)