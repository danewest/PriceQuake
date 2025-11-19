from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import asyncio

from App.api.routes import router as api_router
from App.services.stock_fetcher import ALLOWED_STOCKS
from App.services.timeseries import record_price_point

app = FastAPI()

# --- API router (JSON endpoints) ---
app.include_router(api_router)

# --- Static front-end (HTML/JS/CSS) ---

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=FileResponse)
def root():
    """
    Serve the front-end dashboard.
    """
    return FileResponse(STATIC_DIR / "index.html")


# --- Background price polling (Price Polling Service behavior) ---


async def price_polling_loop():
    """
    Polls prices for a subset of allowed stocks every 5 minutes
    and stores them in the in-memory time-series store.
    """
    # Choose at least 3 symbols to satisfy the requirement
    symbols_to_poll = ALLOWED_STOCKS[:3]

    while True:
        for symbol in symbols_to_poll:
            record_price_point(symbol)
        # 300 seconds = 5 minutes
        await asyncio.sleep(300)


@app.on_event("startup")
async def start_background_tasks():
    """
    On app startup, launch the polling loop in the background.
    """
    asyncio.create_task(price_polling_loop())
