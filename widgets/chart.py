from nicegui import ui

DARK = "#1e1e1e"
LIGHT_TEXT = "#ccc"
GRID = "#333"


class Chart(ui.highchart):
    def __init__(self, ohlc, volume):

        super().__init__(
            {
                "chart": {
                    "backgroundColor": DARK,
                    "style": {"color": LIGHT_TEXT},
                },
                "title": {"style": {"color": LIGHT_TEXT}},
                "rangeSelector": {
                    "allButtonsEnabled": True,
                    "buttonTheme": {
                        "fill": DARK,
                        "stroke": GRID,
                        "style": {"color": LIGHT_TEXT},
                        "states": {
                            "hover": {"fill": GRID},
                            "select": {
                                "fill": "#444",
                                "style": {"color": "#fff"},
                            },
                        },
                    },
                    "inputStyle": {
                        "backgroundColor": DARK,
                        "color": LIGHT_TEXT,
                    },
                    "labelStyle": {"color": LIGHT_TEXT},
                    "buttons": [
                        {
                            "type": "hour",
                            "count": 24 * 30,
                            "text": "1h",
                            "title": "1 Hour",
                            "dataGrouping": {
                                "forced": True,
                                "units": [["hour", [1]]],
                            },
                        },
                        {
                            "type": "day",
                            "count": 60,
                            "text": "4h",
                            "title": "4 Hours",
                            "dataGrouping": {
                                "forced": True,
                                "units": [["hour", [4]]],
                            },
                        },
                        {
                            "type": "day",
                            "count": 90,
                            "text": "D",
                            "title": "1 Day",
                            "dataGrouping": {
                                "forced": True,
                                "units": [["day", [1]]],
                            },
                        },
                    ],
                    "selected": 1,
                },
                "navigator": {
                    "series": {
                        "color": "#446",
                        "lineWidth": 1,
                        "fillOpacity": 0.3,
                    },
                    "xAxis": {
                        "gridLineColor": GRID,
                        "labels": {"style": {"color": LIGHT_TEXT}},
                    },
                },
                "legend": {
                    "enabled": True,
                    "itemStyle": {"color": LIGHT_TEXT},
                },
                "plotOptions": {
                    "candlestick": {
                        "color": "pink",
                        "lineColor": "red",
                        "upColor": "lightgreen",
                        "upLineColor": "green",
                    },
                    "column": {
                        "color": "#446",
                    },
                    "series": {
                        "dataGrouping": {
                            "enabled": True,
                        },
                    },
                },
                "xAxis": {
                    "labels": {"style": {"color": LIGHT_TEXT}},
                    "gridLineColor": GRID,
                },
                "yAxis": [
                    {
                        "labels": {
                            "align": "left",
                            "style": {"color": LIGHT_TEXT},
                        },
                        "height": "80%",
                        "resize": {"enabled": True},
                        "gridLineColor": GRID,
                    },
                    {
                        "labels": {
                            "align": "left",
                            "style": {"color": LIGHT_TEXT},
                        },
                        "top": "80%",
                        "height": "20%",
                        "offset": 0,
                        "gridLineColor": GRID,
                    },
                ],
                "series": [
                    {
                        "type": "candlestick",
                        "id": "aapl",
                        "name": "AAPL Stock Price",
                        "data": ohlc,
                        "dataGrouping": {
                            "enabled": True,
                            "approximation": "ohlc",
                        },
                    },
                    {
                        "type": "column",
                        "id": "aapl-volume",
                        "name": "AAPL Volume",
                        "data": volume,
                        "yAxis": 1,
                        "dataGrouping": {
                            "enabled": True,
                            "approximation": "sum",
                        },
                    },
                    {"type": "wma", "linkedTo": "aapl"},
                    {"type": "wma", "linkedTo": "aapl", "params": {"period": 50}},
                ],
            },
            type="stockChart",
            extras=[
                "stock",
                "indicators",
                "wma",
            ],
        )

    def update_period(self, number):
        self.options["series"][-1]["params"]["period"] = number
