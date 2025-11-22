import asyncio
from fastapi import FastAPI, HTTPException, Query
import yfinance as yf
from datetime import datetime

from App.services.stock_fetcher import get_stock_price, ALLOWED_STOCKS
from App.services.timeseries import record_price_point, get_price_history

app = FastAPI(title="Price Service")

@app.get("/allowed-symbols")
def allowed_symbols():
    return {"symbols": ALLOWED_STOCKS}

@app.get("/price")
def price(symbol: str):
    symbol = symbol.upper()

    # Fetch the current price
    result = get_stock_price(symbol)

    # Also record this as a new time-series point
    try:
        record_price_point(symbol)
    except Exception:
        pass  # don't break if storage fails

    return result


@app.get("/timeseries")
def timeseries(
    symbol: str = Query(..., description="Stock ticker symbol"),
    limit: int = Query(100, ge=1, le=500)
):
    symbol = symbol.upper()
    if symbol not in ALLOWED_STOCKS:
        raise HTTPException(status_code=400, detail="Unsupported symbol")
    return get_price_history(symbol, limit=limit)

async def _polling_loop():
    """
    Background loop: periodically record price points for all allowed symbols.
    """
    symbols_to_poll = ALLOWED_STOCKS
    while True:
        for sym in symbols_to_poll:
            record_price_point(sym)
        # 300 seconds = 5 minutes
        await asyncio.sleep(300)

@app.get("/historical")
def historical(
    symbol: str = Query(..., description="Stock ticker symbol"),
    period: str = Query("1mo", description="yfinance period, e.g. 5d, 1mo, 3mo, 1y"),
    interval: str = Query("1d", description="yfinance interval, e.g. 1m, 5m, 1h, 1d"),
):
    """
    Return historical OHLC data for a symbol over a longer period, using yfinance.

    Example: /historical?symbol=INTC&period=6mo&interval=1d
    """
    symbol = symbol.upper()
    if symbol not in ALLOWED_STOCKS:
        raise HTTPException(status_code=400, detail="Unsupported symbol")

    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch history: {e}")

    if hist.empty:
        return {"symbol": symbol, "points": []}

    points = []
    for ts, row in hist.iterrows():
        points.append({
            "timestamp": ts.to_pydatetime().isoformat(),
            "price": float(row["Close"]),
        })

    return {"symbol": symbol, "points": points}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(_polling_loop())

