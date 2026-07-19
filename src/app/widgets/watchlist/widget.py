
from app.client import YFinanceClient
from app.widgets.watchlist.tabs import StockTabs

from nicegui import ui
from app.widgets.chart.widget import Chart, ChartData
from app.widgets.watchlist.stocklist import StockList, StockInput
from dataclasses import dataclass
from app.models.ticker import Ticker

@dataclass
class Watchlists:
    items: list[Watchlist]

    @property
    def names(self):
        return [x.name for x in self.items]

    @property
    def tickers(self) -> list[Ticker]:
        return [ticker for watchlist in self.items for ticker in watchlist.tickers]


@dataclass
class Watchlist:
    name: str
    tickers: list[Ticker]


class WatchlistWidget:
    def __init__(self):
        self.stocklists: list[StockList] = []
        self.chart_data: ChartData | None = None
        self.watchlists = self.get_watchlists()
        self.load_data()

    def get_watchlists(self) -> Watchlists:
        list1 = Watchlist("First", [Ticker("BRN.AX"), Ticker("DRO.AX")])
        list2 = Watchlist(
            "Second",
            [
                Ticker("APX.AX"),
                Ticker("COH.AX"),
            ],
        )
        return Watchlists([list1, list2])

    def load_data(self):
        tickers = self.watchlists.tickers
        data = YFinanceClient().get_data(tickers)
        for ticker in tickers:
            ticker.chart_data = data[ticker.name]

    def on_ticker_change(self, ticker: Ticker):
        self.chart_data = ticker.chart_data
        if self.chart_data:
            self.chart.update_data(self.chart_data)

    def on_tab_change(self,previous_tab_index: int,  next_tab_index: int):
        self.chart_data = self.stocklists[next_tab_index].selected_ticker.chart_data
        if self.chart_data:
            self.chart.update_data(self.chart_data)
        self.stocklists[previous_tab_index].active = False
        self.stocklists[next_tab_index].active = True

    def build_chart(self):
        if not self.chart_data:
            self.chart_data = self.stocklists[0].selected_ticker.chart_data
            if not self.chart_data:
                return
        with ui.column().classes("w-full h-full"):
            number = ui.number(
                value=20,
                label="Update",
                min=1,
                on_change=lambda e: self.chart.update_period(e.value),
            )
            self.chart = Chart(self.chart_data).classes("w-full h-full")

    def build(self):
        with ui.row().classes('w-full h-full no-wrap'):
            with ui.column().classes("w-1/3"):
                # StockInput(label="Search").classes("w-full")
                tabs = StockTabs(self.watchlists.names, on_change=self.on_tab_change)
                with ui.tab_panels(tabs, value=tabs.named_tabs[0]).classes("w-full"):
                    for idx, watchlist in enumerate(self.watchlists.items):
                        with ui.tab_panel(watchlist.name):
                            stocklist = StockList(
                                watchlist.tickers, on_change=self.on_ticker_change
                            ).classes("w-full")
                            if idx == 0:
                                stocklist.active = True
                            self.stocklists.append(stocklist)

            self.build_chart()


