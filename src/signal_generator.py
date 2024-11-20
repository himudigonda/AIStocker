import pandas as pd

def generate_signals(data):
    if data is None or data.empty:
        return pd.DataFrame()

    # Add Short-term and Long-term Moving Averages
    data['Short_MA'] = data['Close'].rolling(window=10).mean()
    data['Long_MA'] = data['Close'].rolling(window=50).mean()

    # Initialize columns for signals
    data['Signal'] = 0  # Default: No signal
    data['Trade Signal'] = None  # Store Buy/Sell/Hold labels

    # Generate signals: 1 for Buy, -1 for Sell
    data.loc[data['Short_MA'] > data['Long_MA'], 'Signal'] = 1
    data.loc[data['Short_MA'] <= data['Long_MA'], 'Signal'] = -1

    # Generate trading signal based on the change in Signal
    data['Trade Signal'] = data['Signal'].diff()

    data.loc[data['Trade Signal'] == 1, 'Trade Signal'] = "Buy"
    data.loc[data['Trade Signal'] == -1, 'Trade Signal'] = "Sell"
    data.loc[data['Trade Signal'].isnull(), 'Trade Signal'] = "Hold"

    return data[['Close', 'Short_MA', 'Long_MA', 'Signal', 'Trade Signal']]
