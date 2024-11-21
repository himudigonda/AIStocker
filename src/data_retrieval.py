import yfinance as yf

def get_stock_data(symbol, period="8y", interval="1d"):
    """
    Fetch stock data for a given symbol, period, and interval.

    Args:
        symbol (str): Stock ticker symbol (e.g., AAPL)
        period (str): Data period (e.g., '8y')
        interval (str): Data interval (e.g., '1d', '1wk', '1mo')

    Returns:
        DataFrame: Stock data for the specified period and interval
    """
    stock = yf.Ticker(symbol)
    try:
        data = stock.history(period=period, interval=interval)
        if data.empty:
            raise ValueError("No data available for the selected period and interval.")
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol} with period={period} and interval={interval}: {e}")
        return None
