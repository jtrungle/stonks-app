
from typing import TypedDict
from yfinance import EquityQuery
from nicegui import ui
from app.base.keybindbase import KeybindMixin
from nicegui import events

from yfinance.const import EQUITY_SCREENER_FIELDS, EQUITY_SCREENER_EQ_MAP

class QueryModel(TypedDict):
    operator: str
    operands: list[QueryModel]
    

class QueryBuilder(KeybindMixin):
    DEFAULT_SCREENS = [

        EquityQuery("eq", ["region", "us"]),
    ]
    def __init__(self) -> None:
        self.query_models = []
        self.build()

    def handle_key(self, e: events.KeyEventArguments):
        if e.key == "n" and not e.action.repeat:
            if e.action.keydown:
                self.new_query()

    def new_query(self):
        """adds new query model in self.queries and refresh the build"""
        pass

    def build_query(self,query):
        """create the corresponding fields ui input"""
        pass

    @ui.refreshable_method
    def build_queries(self):
        for query in self.query_models:
            self.build_query(query)


    def build(self):
        self.build_queries()

