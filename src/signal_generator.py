import pandas as pd
import logging

def calculate_rsi(series, period=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(series, short_window=12, long_window=26, signal_window=9):
    short_ema = series.ewm(span=short_window, adjust=False).mean()
    long_ema = series.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal_line

def calculate_bollinger_bands(series, window=20, num_std_dev=2):
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()
    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)
    return upper_band, lower_band

def generate_signals(data):
    logger = logging.getLogger(__name__)

    if data is None or data.empty:
        logger.warning("No data provided for signal generation.")
        return pd.DataFrame()

    try:
        logger.info("Generating signals...")

        # Calculate moving averages
        data['Short_MA'] = data['Close'].rolling(window=10).mean()
        data['Long_MA'] = data['Close'].rolling(window=50).mean()

        # Calculate RSI
        data['RSI'] = calculate_rsi(data['Close'])

        # Calculate MACD
        data['MACD'], data['Signal_Line'] = calculate_macd(data['Close'])

        # Calculate Bollinger Bands
        data['Upper_Band'], data['Lower_Band'] = calculate_bollinger_bands(data['Close'])

        # Generate buy/sell signals based on moving averages
        data['Signal'] = 0
        data.loc[data['Short_MA'] > data['Long_MA'], 'Signal'] = 1
        data.loc[data['Short_MA'] <= data['Long_MA'], 'Signal'] = -1
        data['Trade Signal'] = data['Signal'].diff().map({1: 'Buy', -1: 'Sell'}).fillna('Hold')

        logger.info("Signals generated successfully.")
        return data[['Close', 'Short_MA', 'Long_MA', 'RSI', 'MACD', 'Signal_Line', 'Upper_Band', 'Lower_Band', 'Trade Signal']]
    except Exception as e:
        logger.error(f"Error generating signals: {e}")
        return pd.DataFrame()
