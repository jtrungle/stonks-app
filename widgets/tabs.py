from nicegui import ui
from nicegui import events


class StockTabs(ui.tabs):
    def __init__(self, tabs: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tabs = tabs
        self.named_tabs = []
        self.build_tabs()
        self.register_keybinds()
        self.current_tab = 0
        self.next_tab = None

    def handle_key(self, e: events.KeyEventArguments):
        if e.key == "]" and not e.action.repeat:
            if e.action.keydown:
                self.next()

        elif e.key == "[" and not e.action.repeat:
            if e.action.keydown:
                self.previous()

    def next(self):
        self.next_tab = self.current_tab + 1
        self.update_tab()

    def previous(self):
        self.next_tab = self.current_tab - 1
        self.update_tab()

    def update_tab(self):
        if self.next_tab is not None:
            if self.next_tab > len(self.named_tabs) - 1:
                self.next_tab = None
                return
            elif self.next_tab < 0:
                self.next_tab = None
                return
            self.set_value(self.named_tabs[self.next_tab])
            self.current_tab = self.next_tab
            self.next_tab = None


    def register_keybinds(self):
        ui.keyboard(on_key=self.handle_key)

    def build_tabs(self):
        with self:
            for tab in self._tabs:
                tab_widget = ui.tab(tab)
                self.named_tabs.append(tab_widget)
