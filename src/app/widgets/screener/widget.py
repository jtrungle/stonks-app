from typing import TypedDict
from yfinance import EquityQuery
import yfinance as yf
from yfinance.const import EQUITY_SCREENER_FIELDS
from nicegui import ui
from dataclasses import dataclass
from app.base.keybindbase import KeybindMixin
from app.base.list import BaseList, ListItemWidget
from nicegui import events
from nicegui import binding
from app.widgets.screener.querybuilder import QueryBuilder


@dataclass
class ScreenResponse:
    start: int
    count: int
    total: int
    quotes: list[dict]
    useRecords: bool

    @property
    def quote_fields(self):
        fields = set()
        for quote in self.quotes:
            fields.update(quote)
        return list(fields)


class StockList(BaseList[dict]):
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
            ui.item_label("Screen Results").props("header").classes("text-bold")
            ui.separator()
            for item in self.items:
                item_widget = ListItemWidget(on_click=self.on_click)
                with item_widget:
                    with ui.item_section():
                        id = item['symbol']
                        ui.item_label(item['symbol'])
                        item_widget.value = id
                self.item_widgets.append(item_widget)

        self.item_widgets[0].select()



class ScreenerWidget:
    def __init__(self):
        self._active = False

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        if value:
            self.stocklist.active = True
        else:
            self.stocklist.active = False

    def build(self):
        q = EquityQuery(
            "and",
            [
                EquityQuery("gt", ["percentchange", 3]),
                EquityQuery("eq", ["region", "us"]),
            ],
        )

        res = yf.screen(q, sortField="percentchange", sortAsc=True)
        res = ScreenResponse(**res)
        with ui.row().classes('w-full no-wrap'):
            with ui.column().classes('w-1/3 h-full'):
                QueryBuilder()
            with ui.column().classes('w-full h-full'):
                self.stocklist = StockList(res.quotes)

