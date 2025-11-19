from datetime import datetime, timezone
from typing import Dict, List, Any

from App.services.stock_fetcher import get_stock_price, ALLOWED_STOCKS

# In-memory time-series storage: { "AAPL": [ {timestamp, price}, ... ], ... }
_price_history: Dict[str, List[dict]] = {symbol: [] for symbol in ALLOWED_STOCKS}

# Maximum number of points to keep per symbol (you can tune this)
MAX_POINTS_PER_SYMBOL = 500


def record_price_point(symbol: str) -> dict:
    """
    Polls the current price for the given symbol using get_stock_price and
    appends it to the in-memory time series.
    Returns either {"ok": True, "point": {...}} or {"error": "..."}.
    """
    symbol = symbol.upper()
    result = get_stock_price(symbol)

    # If get_stock_price failed, propagate the error
    if "price" not in result:
        # e.g. {"error": "..."}
        return result

    price = result["price"]
    point = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "price": float(price),
    }

    history = _price_history.setdefault(symbol, [])
    history.append(point)

    # Keep history bounded
    if len(history) > MAX_POINTS_PER_SYMBOL:
        history.pop(0)

    return {"ok": True, "point": point}


def get_price_history(symbol: str, limit: int = 100) -> dict:
    """
    Returns the most recent 'limit' points for a given symbol.
    """
    symbol = symbol.upper()
    if symbol not in _price_history:
        return {"error": f"Symbol {symbol} is not supported."}

    history = _price_history[symbol]
    if limit <= 0:
        limit = 1

    return {
        "symbol": symbol,
        "points": history[-limit:],
        "count": len(history[-limit:])
    }
