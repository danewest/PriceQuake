import yfinance as yf
from App.services.stock_fetcher import ALLOWED_STOCKS


def get_fundamentals(symbol: str) -> dict:
    """
    Fetches fundamental metrics for a stock using yfinance.

    Returns either:
      {
        "symbol": "AAPL",
        "longName": "...",
        "marketCap": ...,
        "trailingPE": ...,
        "dividendYield": ...,
        "fiftyTwoWeekHigh": ...,
        "fiftyTwoWeekLow": ...
      }
    or:
      { "error": "..." }
    """
    symbol = symbol.upper()

    if symbol not in ALLOWED_STOCKS:
        return {"error": f"Symbol {symbol} is not supported by PriceQuake."}

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        if not info:
            return {"error": "No fundamental data available for this symbol."}

        return {
            "symbol": symbol,
            "longName": info.get("longName"),
            "marketCap": info.get("marketCap"),
            "trailingPE": info.get("trailingPE"),
            "dividendYield": info.get("dividendYield"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
        }
    except Exception as e:
        # Robust error handling: don’t crash, just return the error
        return {"error": str(e)}
