import yfinance as yf

import logging
import yfinance as yf

def get_stock_data(symbol, period="1y", interval="1d"):
    """
    Fetch stock data for a given symbol, period, and interval.

    Args:
        symbol (str): Stock ticker symbol (e.g., AAPL).
        period (str): Data period (e.g., '1y').
        interval (str): Data interval (e.g., '1d', '1wk', '1mo').

    Returns:
        pd.DataFrame: Stock data for the specified period and interval.
    """
    logger = logging.getLogger(__name__)
    stock = yf.Ticker(symbol)
    try:
        logger.info(f"Fetching data for {symbol} with period={period} and interval={interval}")
        data = stock.history(period=period, interval=interval)

        if data.empty:
            logger.warning(f"No data available for {symbol} with period={period} and interval={interval}")
            return None

        logger.info(f"Data successfully fetched for {symbol}")
        return data
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return None
