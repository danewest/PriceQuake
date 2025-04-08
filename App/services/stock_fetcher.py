from App.db.database import get_connection
import yfinance as yf

# List of permitted stocks. Rather than allowing the user to fetch
# any stocks that they would like, they can use this list of popular
# stocks to allow for development simplicity.
ALLOWED_STOCKS = [
    "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN",
    "META", "NVDA", "NFLX", "INTC", "AMD",
    "DIS", "BA", "JPM", "V", "MA"
]

# Checks Yahoo Finance via the yfinance API for the current price of the requested stock.
# If the price is not available or the stock that was requested is not a member of the
# permitted stocks then it will throw an error.
def get_stock_price(symbol: str):
    if symbol.upper() in ALLOWED_STOCKS:
        try:
            stock = yf.Ticker(symbol)
            price = stock.info.get("regularMarketPrice")

            if price is None:
                return {"error": "Could not retrieve price for this symbol."}
            else:
                return {"price": price}
        except Exception as e:
            return {"error": str(e)}

    else:
        return {"error": "This stock is not supported by PriceQuake."}