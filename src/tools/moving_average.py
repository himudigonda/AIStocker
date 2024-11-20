import yfinance as yf

calculate_moving_average_schema = {
    "name": "calculate_moving_averages",
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

def calculate_moving_averages(symbol, periods):
    stock = yf.Ticker(symbol)
    try:
        data = stock.history(period="1y")
        for period in periods:
            data[f"{period}-Day MA"] = data['Close'].rolling(window=period).mean()
        return data
    except Exception as e:
        return None
