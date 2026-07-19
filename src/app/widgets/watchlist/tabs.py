from nicegui import events

from app.base.tabs import BaseTabs


class StockTabs(BaseTabs):
    def handle_key(self, e: events.KeyEventArguments):
        if e.key == "]" and not e.action.repeat:
            if e.action.keydown:
                self.next()

        elif e.key == "[" and not e.action.repeat:
            if e.action.keydown:
                self.previous()
