# This file is for routing stock fetch calls. While this is not entirely necessary at the moment it will be for future expansion/scalability of the project
from fastapi import APIRouter
from App.services.stock_fetcher import get_stock_price

router = APIRouter()

@router.get("/price")
def fetch_price(symbol: str):
    return get_stock_price(symbol)
