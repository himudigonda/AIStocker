import yfinance as yf
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
    data = stock.history(period=f"{days + 10}d")  # Fetch enough data
    if len(data) < days:
        return None  # Not enough data to calculate moving average
    data['Moving Average'] = data['Close'].rolling(window=days).mean()
    ma = data['Moving Average'].iloc[-1]
    return f"The {days}-day moving average for {symbol} is ${ma:.2f}"
