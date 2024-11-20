import yfinance as yf

calculate_moving_average_schema = {
    "name": "calculate_moving_average",
    "description": "Calculate the moving average for a stock",
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "The stock symbol, e.g. AAPL for Apple",
            },
            "days": {
                "type": "integer",
                "description": "The number of days for the moving average",
            },
        },
        "required": ["symbol", "days"],
    },
}

def calculate_moving_average(symbol, days):
    stock = yf.Ticker(symbol)
    data = stock.history(period=f"{days+1}d")
    ma = data['Close'].rolling(window=days).mean().iloc[-1]
    return f"The {days}-day moving average for {symbol} is ${ma:.2f}"
