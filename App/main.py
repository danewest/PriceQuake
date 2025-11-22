from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from App.api.routes import router as api_router

app = FastAPI(title="PriceQuake Analysis & Visualization Service")

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
