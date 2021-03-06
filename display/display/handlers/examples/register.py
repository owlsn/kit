from display.handlers.base import BaseHandler

class ExamplesRegisterHandler(BaseHandler):
    def get(self):
        title = 'ExamplesRegisterHandler'
        self.render_dict['show_header'] = 0
        self.render_dict['show_aside'] = 0
        self.render_dict['show_footer'] = 0
        self.render('examples/register.html', title = title, **self.render_dict)