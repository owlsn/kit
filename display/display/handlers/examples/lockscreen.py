from display.handlers.base import BaseHandler

class ExamplesLockScreenHandler(BaseHandler):
    def get(self):
        title = 'ExamplesLockScreenHandler'
        self.render_dict['show_header'] = 0
        self.render_dict['show_aside'] = 0
        self.render_dict['show_footer'] = 0
        self.render('examples/lockscreen.html', title = title, **self.render_dict)