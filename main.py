import httpx

from nicegui import ui
from widgets.chart import Chart
from widgets.stocklist import StockList, StockInput
from nicegui import events

data = httpx.get("https://demo-live-data.highcharts.com/aapl-ohlc.json").json()

items = ["101", "BRN", "ASX"]


with ui.row().classes("w-screen h-screen no-wrap"):
    with ui.column().classes("w-1/3"):
        StockInput(label="Search").classes('w-full')
        StockList(items).classes('w-full')

    with ui.column().classes('w-full h-full'):
        number = ui.number(
            value=20, label="Update", min=1, on_change=lambda e: chart.update_period(e.value)
        )
        chart = Chart(data).classes("w-full h-full")

ui.run()
