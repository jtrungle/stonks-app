from nicegui import ui
from app.base.keybindbase import KeybindMixin


class BaseTabs(ui.tabs, KeybindMixin):
    def __init__(self, tabs: list[str], *args, on_change=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._tabs = tabs
        self.named_tabs = []
        self.build_tabs()
        self.register_keybinds()
        self.current_tab = 0
        self.next_tab = None
        self.on_change = on_change

    def next(self):
        self.next_tab = self.current_tab + 1
        self.update_tab()

    def previous(self):
        self.next_tab = self.current_tab - 1
        self.update_tab()

    def update_tab(self):
        if self.next_tab is not None:
            if self.next_tab > len(self.named_tabs) - 1:
                self.next_tab = 0
            elif self.next_tab < 0:
                self.next_tab = len(self.named_tabs) - 1
            self.set_value(self.named_tabs[self.next_tab])
            if self.on_change:
                self.on_change(self.current_tab, self.next_tab)
            self.current_tab = self.next_tab
            self.next_tab = None

    def build_tabs(self):
        with self:
            for tab in self._tabs:
                tab_widget = ui.tab(tab)
                self.named_tabs.append(tab_widget)
