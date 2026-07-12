from nicegui import ui


class Chart(ui.highchart):
    def __init__(self, data):

        super().__init__(
            {
                "rangeSelector": {"selected": 2},
                "legend": {"enabled": True},
                "plotOptions": {
                    "candlestick": {
                        "color": "pink",
                        "lineColor": "red",
                        "upColor": "lightgreen",
                        "upLineColor": "green",
                    },
                },
                "series": [
                    {
                        "type": "candlestick",
                        "id": "aapl",
                        "name": "AAPL Stock Price",
                        "data": data,
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
