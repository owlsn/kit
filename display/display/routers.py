# coding = utf-8
from tornado.routing import URLSpec
from display.handlers.index import *
from display.handlers.calendar import *
from display.handlers.charts import *
from display.handlers.examples import *
from display.handlers.forms import *
import display.handlers.forms as forms
from display.handlers.layout import *
from display.handlers.mailbox import *
from display.handlers.tables import *
from display.handlers.ui import *
import display.handlers.ui as ui
from display.handlers.widgets import *
from display.ui_modules import *

ROUTERS = [
            URLSpec(r'/index1', index1.Index1Handler, name = 'index1'),
            URLSpec(r'/index2', index2.Index2Handler, name = 'index2'),
            URLSpec(r'/calendar', calendar.CalendarHandler, name = 'calendar'),
            URLSpec(r'/charts/chartjs', js.ChartsJsHandler, name = 'chartjs'),
            URLSpec(r'/charts/flot', flot.ChartsFlotHander, name = 'flot'),
            URLSpec(r'/charts/inline', inline.ChartsInlineHander, name = 'inline'),
            URLSpec(r'/charts/morris', morris.ChartsMorrisHander, name = 'morris'),
            URLSpec(r'/examples/404', e404.Examples404Handler, name = '404'),
            URLSpec(r'/examples/500', e500.Examples500Handler, name = '500'),
            URLSpec(r'/examples/blank', blank.ExamplesBlankHandler, name = 'blank'),
            URLSpec(r'/examples/invoice', invoice.ExamplesInvoiceHandler, name = 'invoice'),
            URLSpec(r'/examples/print', iprint.ExamplesPrintHandler, name = 'print'),
            URLSpec(r'/examples/lockscreen', lockscreen.ExamplesLockScreenHandler, name = 'lockscreen'),
            URLSpec(r'/examples/login', login.ExamplesLoginHandler, name = 'login'),
            URLSpec(r'/examples/pace', pace.ExamplesPaceHandler, name = 'pace'),
            URLSpec(r'/examples/profile', profile.ExamplesProfileHandler, name = 'profile'),
            URLSpec(r'/examples/register', register.ExamplesRegisterHandler, name = 'register'),
            URLSpec(r'/forms/advanced', advanced.FormsAdvancedHandler, name = 'advanced'),
            URLSpec(r'/forms/editors', editors.FormsEditorsHandler, name = 'editors'),
            URLSpec(r'/forms/general', forms.general.FormsGeneralHandler, name = 'forms_general'),
            URLSpec(r'/layout/boxed', boxed.LayoutBoxedHandler, name = 'boxed'),
            URLSpec(r'/layout/sidebar', sidebar.LayoutSidebarHandler, name = 'sidebar'),
            URLSpec(r'/layout/fixed', fixed.LayoutFixedHandler, name = 'fixed'),
            URLSpec(r'/layout/nav', nav.LayoutNavHandler, name = 'nav'),
            URLSpec(r'/mailbox/compose', compose.MailboxComposeHandler, name = 'compose'),
            URLSpec(r'/mailbox/mailbox', mailbox.MailboxHandler, name = 'mailbox'),
            URLSpec(r'/mailbox/read', read.MailboxReadHandler, name = 'read'),
            URLSpec(r'/tables/data', data.TablesDataHandler, name = 'data'),
            URLSpec(r'/tables/simple', simple.TablesSimpleHandler, name = 'simple'),
            URLSpec(r'/ui/buttons', buttons.UiButtonsHandler, name = 'buttons'),
            URLSpec(r'/ui/general', ui.general.UiGeneralHandler, name = 'ui_general'),
            URLSpec(r'/ui/icons', icons.UiIconsHandler, name = 'icons'),
            URLSpec(r'/ui/modals', modals.UiModalsHandler, name = 'modals'),
            URLSpec(r'/ui/sliders', sliders.UiSlidersHandler, name = 'sliders'),
            URLSpec(r'/ui/timeline', timeline.UiTimelineHandler, name = 'timeline'),
            URLSpec(r'/widgets', widgets.WidgetsHandler, name = 'widgets'),
        ]

UI_MODULES = {
            'aside' : aside.AsideModule,
            'header' : header.HeaderModule,
            'footer' : footer.FooterModule
        }