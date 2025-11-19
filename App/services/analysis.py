from typing import Dict, List
from App.services.timeseries import get_price_history
from App.services.stock_fetcher import ALLOWED_STOCKS


def compute_sma(symbol: str, window: int = 10) -> dict:
    """
    Computes a Simple Moving Average (SMA) over the most recent 'window'
    prices for the given symbol.

    Returns either:
      { "symbol": "AAPL", "window": 10, "sma": 123.45 }
    or:
      { "error": "..." }
    """
    symbol = symbol.upper()

    if symbol not in ALLOWED_STOCKS:
        return {"error": f"Symbol {symbol} is not supported."}

    # Get enough history for the window
    history_result = get_price_history(symbol, limit=window)

    if "error" in history_result:
        return history_result

    points = history_result.get("points", [])
    if len(points) < window:
        return {"error": f"Not enough data points to compute SMA({window})."}

    prices = [p["price"] for p in points[-window:]]

    sma_value = sum(prices) / window

    return {
        "symbol": symbol,
        "window": window,
        "sma": sma_value
    }
