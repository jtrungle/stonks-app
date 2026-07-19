from nicegui import ui
import abc
from nicegui import events


class KeybindMixin(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle_key(self, e: events.KeyEventArguments):
        pass

    def register_keybinds(self):
        ui.keyboard(on_key=self.handle_key)
