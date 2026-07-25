import random
import time

from app.models.ticker import Ticker
from app.widgets.chart.widget import ChartData

_MOCK_PRICES: dict[str, tuple[float, float]] = {
    "BRN.AX": (0.35, 0.05),
    "DRO.AX": (0.90, 0.10),
    "APX.AX": (1.20, 0.15),
    "COH.AX": (2.50, 0.30),
}

_MOCK_POINTS = 24
_HOUR_MS = 3_600_000


def _generate_ohlcv(base_price: float, volatility: float) -> tuple[list[list], list[list]]:
    rng = random.Random(base_price * 1000)
    now = int(time.time() * 1000)
    start = now - _MOCK_POINTS * _HOUR_MS

    ohlc: list[list] = []
    volume: list[list] = []
    price = base_price

    for i in range(_MOCK_POINTS):
        ts = start + i * _HOUR_MS
        change = rng.uniform(-volatility, volatility)
        close = max(price + change, base_price * 0.5)
        open_price = close - rng.uniform(-volatility * 0.6, volatility * 0.6)
        high = max(open_price, close) + abs(rng.uniform(0, volatility * 0.4))
        low = min(open_price, close) - abs(rng.uniform(0, volatility * 0.4))
        ohlc.append([ts, round(open_price, 4), round(high, 4), round(low, 4), round(close, 4)])
        vol = int(rng.uniform(50_000, 500_000))
        volume.append([ts, vol])
        price = close

    return ohlc, volume


def get_mock_chart_data(tickers: list[Ticker]) -> dict[str, ChartData]:
    result: dict[str, ChartData] = {}
    for ticker in tickers:
        if ticker.name in _MOCK_PRICES:
            base, vol = _MOCK_PRICES[ticker.name]
        else:
            base, vol = 1.0, 0.1
        ohlc, volume = _generate_ohlcv(base, vol)
        result[ticker.name] = ChartData(ohlc, volume)
    return result


MOCK_SCREEN_RESPONSE: dict = {
    "start": 0,
    "count": 4,
    "total": 4,
    "quotes": [
        {"symbol": "NVDA", "shortName": "NVIDIA Corporation", "regularMarketPrice": 180.50, "regularMarketChangePercent": 5.2},
        {"symbol": "AMD", "shortName": "Advanced Micro Devices", "regularMarketPrice": 120.30, "regularMarketChangePercent": 3.8},
        {"symbol": "INTC", "shortName": "Intel Corporation", "regularMarketPrice": 32.10, "regularMarketChangePercent": 4.1},
        {"symbol": "TSM", "shortName": "Taiwan Semiconductor", "regularMarketPrice": 210.75, "regularMarketChangePercent": 6.3},
    ],
    "useRecords": False,
}
