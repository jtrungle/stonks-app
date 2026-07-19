from yfinance import EquityQuery
import yfinance as yf
from yfinance.const import EQUITY_SCREENER_FIELDS
from nicegui import ui
from dataclasses import dataclass


@dataclass
class ScreenResponse:
    start: int
    count: int
    total: int
    quotes: list[dict]
    useRecords: bool


class ScreenerWidget:
    def __init__(self):
        pass

    def build(self):
        ui.label("Screener")
        q = EquityQuery(
            "and",
            [
                EquityQuery("gt", ["percentchange", 3]),
                EquityQuery("eq", ["region", "us"]),
            ],
        )
        res = yf.screen(q, sortField="percentchange", sortAsc=True)
        res = ScreenResponse(**res)
        ui.table(rows=res.quotes, selection="single")

