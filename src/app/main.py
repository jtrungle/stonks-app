
from nicegui import ui

from app.base.tabs import BaseTabs
from nicegui import events
from app.widgets.watchlist.widget import WatchlistWidget

class MainTabs(BaseTabs):
    def handle_key(self, e: events.KeyEventArguments):
        if e.key == "Tab" and not e.action.repeat:
            if e.action.keydown:
                self.next()

        if e.modifiers.shift and e.action.keydown:
            if e.key == "Tab" and not e.action.repeat:
                if e.action.keydown:
                    self.previous()


tabs = MainTabs(['Watchlist', "Screener"])
with ui.tab_panels(tabs, value=tabs.named_tabs[0]).classes("w-full h-screen"):
    with ui.tab_panel("Watchlist"):
        WatchlistWidget().build()

    with ui.tab_panel("Screener"):
        ui.label('Screener')
ui.dark_mode(True)
ui.run(show=False)
