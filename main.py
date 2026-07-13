from widgets.tabs import StockTabs
import httpx

from nicegui import ui
from widgets.chart import Chart
from widgets.stocklist import StockList, StockInput
from nicegui import events
import yfinance as yf

data = httpx.get("https://demo-live-data.highcharts.com/aapl-ohlc.json").json()
# d
df = yf.download(tickers="AAPL", interval="1h", period="6mo")
df.columns = df.columns.get_level_values(0)
df = df.reset_index()
df["Datetime"] = df["Datetime"].astype("int64") * 1000
ohlc = df[["Datetime", "Open", "High", "Low", "Close"]].to_dict(orient='split')['data']
volume = df[["Datetime", "Volume"]].to_dict(orient='split')['data']

data = []

items = ["101", "BRN", "ASX"]


with ui.row().classes("w-screen h-screen no-wrap"):
    with ui.column().classes("w-1/3"):
        StockInput(label="Search").classes("w-full")
        tabs = StockTabs(["Watchlist", "Watchlist 2"])
        with ui.tab_panels(tabs, value=tabs.named_tabs[0]).classes("w-full"):
            with ui.tab_panel(tabs.named_tabs[0]):
                StockList(items).classes("w-full")
            with ui.tab_panel(tabs.named_tabs[1]):
                ui.label("Infos")

    with ui.column().classes("w-full h-full"):
        number = ui.number(
            value=20,
            label="Update",
            min=1,
            on_change=lambda e: chart.update_period(e.value),
        )
        chart = Chart(ohlc, volume).classes("w-full h-full")

ui.dark_mode(True)
ui.run(show=False)
