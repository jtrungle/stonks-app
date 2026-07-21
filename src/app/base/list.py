from app.base.keybindbase import KeybindMixin
from nicegui import ui
from nicegui import events
from typing import Any, TypeVar
import abc
from typing import Generic

IT = TypeVar("IT")


class ListItemWidget(ui.item):
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


class BaseList(ui.list, KeybindMixin, Generic[IT], metaclass=abc.ABCMeta):
    def __init__(self, items: list[IT], *args, on_change=None, **kwargs):
        self.selected_index = 0
        self.next_index = None
        self.on_change = on_change
        super().__init__(*args, **kwargs)
        self.props("bordered separator")
        self.item_widgets: list[ListItemWidget] = []
        self.items = items
        self.build()
        self.register_keybinds()
        self.active = False

    @property
    def selected_item(self) -> IT:
        return self.items[self.selected_index]

    def next(self):

        self.next_index = self.selected_index + 1
        self.update_widget()

    def previous(self):
        self.next_index = self.selected_index - 1
        self.update_widget()

    def update_widget(self):
        if self.next_index is not None:
            if self.next_index > len(self.item_widgets) - 1:
                self.next_index = 0

            elif self.next_index < 0:
                self.next_index = len(self.item_widgets) - 1
            current_widget = self.item_widgets[self.selected_index]
            current_widget.unselect()
            next_widget = self.item_widgets[self.next_index]
            next_widget.select()
            self.selected_index = self.next_index
            self.next_index = None
        if self.on_change:
            self.on_change(self.selected_item)

    def handle_key(self, e: events.KeyEventArguments):
        if self.active:
            if e.key == "j" and not e.action.repeat:
                if e.action.keydown:
                    self.next()

            if e.key == "k" and not e.action.repeat:
                if e.action.keydown:
                    self.previous()

    def on_click(self, e):

        self.next_index = self.item_widgets.index(e.sender)
        self.update_widget()

    @abc.abstractmethod
    def build(self): ...
