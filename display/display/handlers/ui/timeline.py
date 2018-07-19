from display.handlers.base import BaseHandler

class UiTimelineHandler(BaseHandler):
    def get(self):
        title = 'UiTimelineHandler'
        self.render('ui/timeline.html', title = title, **self.render_dict)