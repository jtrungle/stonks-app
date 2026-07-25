# AGENTS.md

## Stack
- **NiceGUI** (Python web UI framework, single-process desktop app)
- **yfinance** — stock data, **Highcharts** (via `nicegui[highcharts]`) — candlestick charts
- **pandas** — data manipulation
- **Python 3.14+, uv** for packaging, **ruff** for linting (no config = defaults)

## Commands

| Action | Command |
|---|---|
| Run app | `uv run app` or `python -m app.main` |
| Lint | `uv run ruff check` |
| Format | `uv run ruff format` |

## Structure

```
src/app/
├── main.py              # Entrypoint — creates App, calls .build(), ui.run()
├── client.py            # YFinanceClient — fetches OHLCV via yfinance.download()
├── base/                # Reusable UI mixins (keybind, tabs, list, state)
├── models/ticker.py     # Ticker dataclass
└── widgets/
    ├── chart/           # Highcharts candlestick + volume chart
    ├── watchlist/       # Watchlist tab (hardcoded tickers: BRN.AX, DRO.AX, etc.)
    └── screener/        # Screener tab (yfinance.EquityQuery + yf.screen())
```

## Key facts

- **No tests** exist. No CI/CD.
- `widgets/` at repo root is a stale artifact (only `__pycache__`). Ignore it.
- Keyboard nav: `j`/`k` move up/down lists, `Tab`/`Shift+Tab` or `[`/`]` switch tabs.
- VS Code launch config at `.vscode/launch.json` runs `python -m app.main`.
- Watchlist tickers are hardcoded in `widgets/watchlist/`.
