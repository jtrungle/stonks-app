import yfinance as yf

from app.widgets.chart.widget import ChartData
from app.models.ticker import Ticker
from app.exceptions import NoDataFoundError

class YFinanceClient:
    def __init__(self) -> None:
        pass

    def get_data(self, tickers: list[Ticker]) -> dict[str, ChartData]:

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
