import yfinance as yf

get_stock_price_schema = {
    "name": "get_stock_price",
    "description": "Get the current stock price for a given symbol",
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "The stock symbol, e.g. AAPL for Apple",
            },
        },
        "required": ["symbol"],
    },
}

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    current_price = stock.history(period="1d")['Close'].iloc[-1]
    return f"The current stock price of {symbol} is ${current_price:.2f}"
