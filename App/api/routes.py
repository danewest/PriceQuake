# This file defines the API surface of the Analysis & Visualization Service.

import os

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import httpx

router = APIRouter()

# Base URLs for the other microservices. These are set in docker-compose for
# containerized deployment, but we provide sensible defaults for local dev.
PRICE_SERVICE_URL = os.getenv("PRICE_SERVICE_URL", "http://price-service:8001")
FUND_SERVICE_URL = os.getenv("FUND_SERVICE_URL", "http://fundamentals-service:8002")


@router.get("/price")
def fetch_price(symbol: str):
    """
    Current price endpoint.

    Delegates to the Price Polling Service.
    """
    symbol = symbol.upper()

    try:
        resp = httpx.get(f"{PRICE_SERVICE_URL}/price", params={"symbol": symbol})
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Price service unavailable: {exc}")

    if resp.status_code != 200:
        # Try to propagate a useful error message from the downstream service
        try:
            detail = resp.json().get("detail", "Price service error")
        except Exception:
            detail = "Price service error"
        raise HTTPException(status_code=resp.status_code, detail=detail)

    return resp.json()


@router.get("/allowed-symbols")
def allowed_symbols():
    """
    Returns the list of allowed stock tickers for the UI to display.

    Delegates to the Price Polling Service.
    """
    try:
        resp = httpx.get(f"{PRICE_SERVICE_URL}/allowed-symbols")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Price service unavailable: {exc}")

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Price service error")

    return resp.json()


@router.get("/timeseries")
def timeseries(symbol: str, limit: int = Query(100, ge=1, le=500)):
    """
    Returns recent time-series price data for a symbol.

    Data is populated by the background polling loop in the Price Polling Service.
    """
    symbol = symbol.upper()

    try:
        resp = httpx.get(
            f"{PRICE_SERVICE_URL}/timeseries",
            params={"symbol": symbol, "limit": limit},
        )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Price service unavailable: {exc}")

    if resp.status_code != 200:
        try:
            detail = resp.json().get("detail", "Price service error")
        except Exception:
            detail = "Price service error"
        raise HTTPException(status_code=resp.status_code, detail=detail)

    return resp.json()


@router.get("/fundamentals")
def fundamentals(symbol: str):
    """
    Returns fundamental metrics (market cap, P/E, etc.) for a symbol.

    Delegates to the Fundamentals Service, but *never* throws just because
    fundamentals are missing. It returns { error: ... } instead.
    """
    symbol = symbol.upper()

    try:
        resp = httpx.get(
            f"{FUND_SERVICE_URL}/fundamentals",
            params={"symbol": symbol},
            timeout=5.0,
        )
    except httpx.RequestError as exc:
        # Fundamentals service unreachable → return an error object, 200 OK
        return {"error": f"Fundamentals service unavailable: {exc}"}

    if resp.status_code != 200:
        # Try to extract the detail, but again, just return an error object
        try:
            detail = resp.json().get("detail", "Fundamentals service error")
        except Exception:
            detail = "Fundamentals service error"
        return {"error": detail}

    return resp.json()



@router.get("/analysis/sma")
def sma(symbol: str, window: int = Query(10, ge=2, le=200)):
    """
    Technical indicator endpoint: Simple Moving Average (SMA).

    Computes SMA using the time-series data stored in the Price Polling Service.
    If the price service is down or we don't have enough points yet,
    we return a valid JSON object with sma=None instead of raising.
    """
    symbol = symbol.upper()

    # Default "empty" response — we return this on errors instead of raising
    base_response = {
        "symbol": symbol,
        "window": window,
        "sma": None,
        "points_used": 0,
        "error": None,
    }

    try:
        resp = httpx.get(
            f"{PRICE_SERVICE_URL}/timeseries",
            params={"symbol": symbol, "limit": window * 2},
            timeout=5.0,
        )
    except httpx.RequestError as exc:
        base_response["error"] = f"Price service unavailable: {exc}"
        return base_response

    if resp.status_code != 200:
        try:
            detail = resp.json().get("detail", "Price service error")
        except Exception:
            detail = "Price service error"
        base_response["error"] = detail
        return base_response

    data = resp.json()
    points = data.get("points", [])

    if not points:
        base_response["error"] = "No time-series data available yet."
        return base_response

    # If we don't have enough points, just use what we have
    window_used = min(window, len(points))
    prices = [p["price"] for p in points[-window_used:]]
    sma_value = sum(prices) / window_used

    return {
        "symbol": symbol,
        "window": window_used,
        "sma": sma_value,
        "points_used": window_used,
        "error": None,
    }




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

    price_result = fetch_price(symbol)
    timeseries_result = timeseries(symbol=symbol, limit=limit)
    sma_result = sma(symbol=symbol, window=window)
    fundamentals_result = fundamentals(symbol=symbol)

    return {
        "symbol": symbol,
        "price": price_result,
        "timeseries": timeseries_result,
        "sma": sma_result,
        "fundamentals": fundamentals_result,
    }

@router.get("/historical-timeseries")
def historical_timeseries(
    symbol: str,
    period: str = Query("1mo"),
    interval: str = Query("1d"),
):
    """
    Analysis-service wrapper around the Price Service /historical endpoint.
    """
    symbol = symbol.upper()
    try:
        resp = httpx.get(
            f"{PRICE_SERVICE_URL}/historical",
            params={"symbol": symbol, "period": period, "interval": interval},
            timeout=10.0,
        )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Price service unavailable: {exc}")

    if resp.status_code != 200:
        try:
            detail = resp.json().get("detail", "Price service error")
        except Exception:
            detail = "Price service error"
        raise HTTPException(status_code=resp.status_code, detail=detail)

    return resp.json()

