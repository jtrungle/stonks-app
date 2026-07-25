import os
from dataclasses import dataclass

import yfinance as yf
from yfinance import EquityQuery

from app.widgets.chart.widget import ChartData
from app.models.ticker import Ticker
from app.exceptions import NoDataFoundError

DEV_MODE = os.environ.get("APP_ENV") == "dev"


@dataclass
class ScreenResponse:
    start: int
    count: int
    total: int
    quotes: list[dict]
    useRecords: bool

    @property
    def quote_fields(self):
        fields = set()
        for quote in self.quotes:
            fields.update(quote)
        return list(fields)


class YFinanceClient:
    def __init__(self) -> None:
        pass

    def get_data(self, tickers: list[Ticker]) -> dict[str, ChartData]:
        if DEV_MODE:
            from app.mock import get_mock_chart_data

            return get_mock_chart_data(tickers)

        ticker_str = [x.name for x in tickers]
        df = yf.download(tickers=ticker_str, interval="1h", period="6mo", group_by="ticker")
        if df is None or df.empty:
            raise NoDataFoundError
        ticker_data = {ticker: df[ticker] for ticker in df.columns.levels[0]}
        for ticker, df in ticker_data.items():
            df = df.reset_index()
            df["Datetime"] = df["Datetime"].astype("int64") * 1000
            ohlc = df[["Datetime", "Open", "High", "Low", "Close"]].to_dict(orient="split")[
                "data"
            ]
            volume = df[["Datetime", "Volume"]].to_dict(orient="split")["data"]
            ticker_data[ticker] = ChartData(ohlc, volume)

        return ticker_data

    def screen(self, query: EquityQuery) -> ScreenResponse:
        if DEV_MODE:
            from app.mock import MOCK_SCREEN_RESPONSE

            return ScreenResponse(**MOCK_SCREEN_RESPONSE)

        res = yf.screen(query, sortField="percentchange", sortAsc=True)
        return ScreenResponse(**res)
