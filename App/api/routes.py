from fastapi import APIRouter
from App.services.stock_fetcher import get_stock_price

router = APIRouter()

@router.get("/price")
def fetch_price(symbol: str):
    return get_stock_price(symbol)
