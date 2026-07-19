from dataclasses import dataclass
from app.widgets.chart.widget import ChartData


@dataclass
class Ticker:
    name: str
    chart_data: ChartData | None = None
