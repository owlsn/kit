from display.handlers.base import BaseHandler

class CalendarHandler(BaseHandler):
    def get(self):
        title = 'CalendarHandler'
        self.render('calendar/calendar.html', title = title, **self.render_dict)