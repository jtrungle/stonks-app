
from nicegui import ui

from app.base.tabs import BaseTabs
from nicegui import events
from app.widgets.screener.widget import ScreenerWidget
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

class App:
    def __init__(self) -> None:
        self.watchlist: WatchlistWidget
        self.screener: ScreenerWidget
        self.widgets = []

    def on_tab_change(self,previous_tab_index: int,  next_tab_index: int):
        self.widgets[previous_tab_index].active = False
        self.widgets[next_tab_index].active = True
    def build(self):
        tabs = MainTabs(['Watchlist', "Screener"],on_change=self.on_tab_change)
        with ui.tab_panels(tabs, value=tabs.named_tabs[0]).classes("w-full h-screen"):
            with ui.tab_panel("Watchlist"):
                self.watchlist = WatchlistWidget()
                self.watchlist.build()
                self.widgets.append(self.watchlist)

            with ui.tab_panel("Screener"):
                self.screener = ScreenerWidget()
                self.screener.build()
                self.widgets.append(self.screener)
App().build()
ui.dark_mode(True)
ui.run(show=False)
