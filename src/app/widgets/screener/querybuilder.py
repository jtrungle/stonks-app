
from typing import TypedDict, get_args
from yfinance import EquityQuery
from nicegui import ui
from app.base.keybindbase import KeybindMixin
from nicegui import events

from yfinance.const import EQUITY_SCREENER_FIELDS, EQUITY_SCREENER_EQ_MAP
from yfinance.screener.query import Operator
from nicegui import binding
from typing import Any
from collections.abc import Callable
from dataclasses import field




@binding.bindable_dataclass
class QueryModel:
    operator: Operator = 'eq'
    category: str = "region"
    query: str = "region"
    values: list[Any] = field(default_factory=list)

class QueryBuilder(KeybindMixin):
    DEFAULT_SCREENS = [
        {"eq": ["region", "au"]},
    ]
    def __init__(self, on_change: Callable | None = None) -> None:
        self.query_models = []
        self.query_dicts = []
        self.load_query_models()
        self.build()

    def load_query_models(self):
        if not self.query_dicts:
            for screen in self.DEFAULT_SCREENS:
                for k, v in screen.items():
                    query_obj = QueryModel(operator=k,category="",query=v[0],values=v[1:])
                    self.query_models.append(query_obj)

    def handle_key(self, e: events.KeyEventArguments):
        if e.key == "n" and not e.action.repeat:
            if e.action.keydown:
                self.new_query()

    def get_category_options(self, value):
        if value == "eq":
            return list(EQUITY_SCREENER_FIELDS['eq_fields'])
        else:
            return list(EQUITY_SCREENER_FIELDS.keys())

    def new_query(self):
        """adds new query model in self.queries and refresh the build"""
        pass

    def build_query(self,query: QueryModel):
        """create the corresponding fields ui input"""
        with ui.row().classes('w-full'):
            ui.select(options=list(get_args(Operator)), value="eq").bind_value(query,"operator")
            ui.select(options=self.get_category_options(query.operator), value='region').bind_value(query,"category")
            ui.select(options=list(EQUITY_SCREENER_FIELDS[query.category]), value='region').bind_value(query,"field")
            ui.input_chips('Values').bind_value(query,'values')

    @ui.refreshable_method
    def build_queries(self):
        for query in self.query_models:
            self.build_query(query)


    def build(self):
        self.build_queries()

