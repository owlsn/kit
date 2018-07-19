from display.handlers.base import BaseHandler

class LayoutSidebarHandler(BaseHandler):
    def get(self):
        title = 'LayoutSidebarHandler'
        self.render('layout/collapsed-sidebar.html', title = title, **self.render_dict)