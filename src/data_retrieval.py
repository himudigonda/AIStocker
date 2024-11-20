import yfinance as yf

def get_stock_data(symbol, period="1y"):
    stock = yf.Ticker(symbol)
    try:
        data = stock.history(period=period)
        return data if not data.empty else None
    except Exception as e:
        return None  # Handle API issues or invalid symbols
