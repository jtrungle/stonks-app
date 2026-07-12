from nicegui import ui
from nicegui import events


class StockInput(ui.input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_keybinds()

    def focus(self):
        self.run_method("focus")

    def handle_key(self, e: events.KeyEventArguments):
        if e.key == "/" and not e.action.repeat:
            if e.action.keydown:
                self.focus()

    def configure_keybinds(self):
        ui.keyboard(on_key=self.handle_key)


class Stock(ui.item):
    def __init__(self, *args, **kwargs):
        self.selected = False
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


class StockList(ui.list):
    def __init__(self, items, *args, callback=None, **kwargs):
        self.selected_index = 0
        self.next_index = None
        self.callback = callback
        super().__init__(*args, **kwargs)
        self.props("bordered separator")
        self.items: list[Stock] = []
        self.build(items)
        self.configure_keybinds()

    def next(self):

        self.next_index = self.selected_index + 1
        self.update()

    def previous(self):
        self.next_index = self.selected_index - 1
        self.update()

    def update(self):
        if self.next_index is not None:
            if self.next_index > len(self.items) - 1:
                self.next_index = None
                return

            elif self.next_index < 0:
                self.next_index = None
                return
            current_widget = self.items[self.selected_index]
            current_widget.unselect()
            next_widget = self.items[self.next_index]
            next_widget.select()
            self.selected_index = self.next_index
            self.next_index = None

    def handle_key(self, e: events.KeyEventArguments):
        if e.key == "j" and not e.action.repeat:
            if e.action.keydown:
                self.next()

        if e.key == "k" and not e.action.repeat:
            if e.action.keydown:
                self.previous()

    def configure_keybinds(self):
        ui.keyboard(on_key=self.handle_key)

    def on_click(self, e):

        self.next_index = self.items.index(e.sender)
        self.update()

    def build(self, items):
        with self:
            ui.item_label("Watchlist").props("header").classes("text-bold")
            ui.separator()
            for item in items:
                item_widget = Stock(on_click=self.on_click)
                with item_widget:
                    with ui.item_section():
                        ui.item_label(item)
                        ui.item_label("name").props("caption")
                self.items.append(item_widget)

        self.items[0].select()
