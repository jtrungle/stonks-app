from app.base.keybindbase import KeybindMixin
from nicegui import ui
from nicegui import events
from app.models.ticker import Ticker


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


class StockItem(ui.item):
    def __init__(self, *args, value=None, **kwargs):
        self.selected = False
        self.value = value

        super().__init__(*args, **kwargs)

    def select(self):
        self.selected = True
        self.update()

    def unselect(self):
        self.selected = False
        self.update()

    def update(self):
        with self.props.suspend_updates():
            if self.selected:
                self.props("active")
            else:
                self.props(remove="active")
            super().update()


class StockList(ui.list, KeybindMixin):
    def __init__(self, tickers: list[Ticker], *args, on_change=None, **kwargs):
        self.selected_index = 0
        self.next_index = None
        self.on_change = on_change
        super().__init__(*args, **kwargs)
        self.props("bordered separator")
        self.items: list[StockItem] = []
        self.tickers: list[Ticker] = tickers
        self.build(tickers)
        self.register_keybinds()
        self.active = False

    @property
    def selected_ticker(self) -> Ticker:
        return self.tickers[self.selected_index]

    def next(self):

        self.next_index = self.selected_index + 1
        self.update_widget()

    def previous(self):
        self.next_index = self.selected_index - 1
        self.update_widget()

    def update_widget(self):
        if self.next_index is not None:
            if self.next_index > len(self.items) - 1:
                self.next_index = 0

            elif self.next_index < 0:
                self.next_index = len(self.items) - 1
            current_widget = self.items[self.selected_index]
            current_widget.unselect()
            next_widget = self.items[self.next_index]
            next_widget.select()
            self.selected_index = self.next_index
            self.next_index = None
        if self.on_change:
            self.on_change(self.selected_ticker)

    def handle_key(self, e: events.KeyEventArguments):
        if self.active:
            if e.key == "j" and not e.action.repeat:
                if e.action.keydown:
                    self.next()

            if e.key == "k" and not e.action.repeat:
                if e.action.keydown:
                    self.previous()

    def on_click(self, e):

        self.next_index = self.items.index(e.sender)
        self.update_widget()

    def build(self, tickers: list[Ticker]):
        with self:
            ui.item_label("Watchlist").props("header").classes("text-bold")
            ui.separator()
            for item in tickers:
                item_widget = StockItem(on_click=self.on_click)
                with item_widget:
                    with ui.item_section():
                        ui.item_label(item.name)
                        ui.item_label("name").props("caption")
                        item_widget.value = item.name
                self.items.append(item_widget)

        self.items[0].select()
