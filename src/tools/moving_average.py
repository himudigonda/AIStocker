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
    try:
        period = "max" if days > 730 else "2y"  # Choose max for large days
        data = stock.history(period=period)

        if len(data) < days:
            return None

        data['Moving Average'] = data['Close'].rolling(window=days).mean()
        ma = data['Moving Average'].iloc[-1]
        return f"The {days}-day moving average for {symbol} is ${ma:.2f}"
    except Exception as e:
        return f"Error calculating moving average for {symbol}: {str(e)}"
