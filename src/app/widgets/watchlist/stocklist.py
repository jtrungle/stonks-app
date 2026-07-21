from app.base.keybindbase import KeybindMixin
from nicegui import ui
from nicegui import events
from app.models.ticker import Ticker
from app.base.list import BaseList, ListItemWidget


class StockInput(ui.input, KeybindMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_keybinds()

    def focus(self):
        self.run_method("focus")

    def handle_key(self, e: events.KeyEventArguments):
        if e.key == "/" and not e.action.repeat:
            if e.action.keydown:
                self.focus()



class StockList(BaseList[Ticker]):
    def handle_key(self, e: events.KeyEventArguments):
        if self.active:
            if e.key == "j" and not e.action.repeat:
                if e.action.keydown:
                    self.next()

            if e.key == "k" and not e.action.repeat:
                if e.action.keydown:
                    self.previous()

    def build(self):
        with self:
            ui.item_label("Watchlist").props("header").classes("text-bold")
            ui.separator()
            for item in self.items:
                item_widget = ListItemWidget(on_click=self.on_click)
                with item_widget:
                    with ui.item_section():
                        ui.item_label(item.name)
                        ui.item_label("name").props("caption")
                        item_widget.value = item.name
                self.item_widgets.append(item_widget)

        self.item_widgets[0].select()
