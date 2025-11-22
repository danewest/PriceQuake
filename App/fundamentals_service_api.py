from fastapi import FastAPI, HTTPException, Query
from App.services.fundamentals import get_fundamentals
from App.services.stock_fetcher import ALLOWED_STOCKS

app = FastAPI(title="Fundamentals Service")


@app.get("/fundamentals")
def fundamentals(symbol: str = Query(..., description="Stock ticker symbol")):
    """
    Fundamentals microservice.

    Always returns 200 with either:
      { ...fundamental fields... }
    or
      { "error": "..." }

    so that downstream services /dashboard-data don't blow up the UI.
    """
    symbol = symbol.upper()

    # Only hard-fail on truly invalid symbols
    if symbol not in ALLOWED_STOCKS:
        raise HTTPException(status_code=400, detail="Unsupported symbol")

    result = get_fundamentals(symbol)

    # IMPORTANT: do NOT raise on result["error"] here.
    # We just return it and let the analysis-service/frontend display "N/A".
    return result
