from nicegui import ui


class Chart(ui.highchart):
    def __init__(self, ohlc, volume):

        super().__init__(
            {
                "rangeSelector": {
                    "buttons": [
                        {
                            "text": "1h",
                            "title": "1 Hour",
                            "dataGrouping": {"units": [["hour", [1]]]},
                        },
                        {
                            "text": "4h",
                            "title": "4 Hours",
                            "dataGrouping": {"units": [["hour", [4]]]},
                        },
                        {
                            "text": "D",
                            "title": "1 Day",
                            "dataGrouping": {"units": [["day", [1]]]},
                        },
                    ],
                    "selected": 1,
                },
                "legend": {"enabled": True},
                "plotOptions": {
                    "candlestick": {
                        "color": "pink",
                        "lineColor": "red",
                        "upColor": "lightgreen",
                        "upLineColor": "green",
                    },
                },
                "yAxis": [
                    {
                        "labels": {"align": "left"},
                        "height": "80%",
                        "resize": {"enabled": True},
                    },
                    {
                        "labels": {"align": "left"},
                        "top": "80%",
                        "height": "20%",
                        "offset": 0,
                    },
                ],
                "series": [
                    {
                        "type": "candlestick",
                        "id": "aapl",
                        "name": "AAPL Stock Price",
                        "data": ohlc,
                    },
                    {
                        "type": "column",
                        "id": "aapl-volume",
                        "name": "AAPL Volume",
                        "data": volume,
                        "yAxis": 1,
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
