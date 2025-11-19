# This file is for routing stock fetch calls. While this is not entirely necessary at the moment it will be for future expansion/scalability of the project
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from App.services.stock_fetcher import get_stock_price, ALLOWED_STOCKS
from App.services.timeseries import get_price_history
from App.services.fundamentals import get_fundamentals
from App.services.analysis import compute_sma

router = APIRouter()


@router.get("/price")
def fetch_price(symbol: str):
    """
    Current price endpoint (reuses existing stock_fetcher logic).
    """
    result = get_stock_price(symbol)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/allowed-symbols")
def allowed_symbols():
    """
    Returns the list of allowed stock tickers for the UI to display.
    """
    return {"symbols": ALLOWED_STOCKS}


@router.get("/timeseries")
def timeseries(symbol: str, limit: int = Query(100, ge=1, le=500)):
    """
    Returns recent time-series price data for a symbol.
    Data is populated by the background polling loop.
    """
    result = get_price_history(symbol, limit=limit)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/fundamentals")
def fundamentals(symbol: str):
    """
    Returns fundamental metrics (market cap, P/E, etc.) for a symbol.
    """
    result = get_fundamentals(symbol)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/analysis/sma")
def sma(symbol: str, window: int = Query(10, ge=2, le=200)):
    """
    Technical indicator endpoint: Simple Moving Average (SMA).
    """
    result = compute_sma(symbol, window=window)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/dashboard-data")
def dashboard_data(
    symbol: str,
    window: int = Query(10, ge=2, le=200),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Fusion endpoint: combine everything the front-end needs onto one screen.

    Returns:
    {
      "symbol": "...",
      "price": { "price": ... },
      "timeseries": { "points": [...] },
      "sma": { "window": ..., "sma": ... },
      "fundamentals": { ... }
    }
    """
    symbol = symbol.upper()

    price_result = get_stock_price(symbol)
    timeseries_result = get_price_history(symbol, limit=limit)
    sma_result = compute_sma(symbol, window=window)
    fundamentals_result = get_fundamentals(symbol)

    # We don't hard-fail the whole response if one part is missing;
    # the front-end can decide what to show.
    return {
        "symbol": symbol,
        "price": price_result,
        "timeseries": timeseries_result,
        "sma": sma_result,
        "fundamentals": fundamentals_result,
    }
