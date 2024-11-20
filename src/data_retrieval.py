import yfinance as yf

def get_stock_data(symbol, period="1y"):
    stock = yf.Ticker(symbol)
    return stock.history(period=period)
