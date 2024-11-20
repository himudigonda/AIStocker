import pandas as pd

def generate_signals(data):
    if data is None or data.empty:
        return pd.DataFrame()  # Return empty if no data

    data['Short_MA'] = data['Close'].rolling(window=10).mean()
    data['Long_MA'] = data['Close'].rolling(window=50).mean()
    data['Signal'] = 0
    data['Signal'][data['Short_MA'] > data['Long_MA']] = 1
    data['Signal'][data['Short_MA'] <= data['Long_MA']] = -1
    data['Trade Signal'] = data['Signal'].diff()
    return data[['Close', 'Short_MA', 'Long_MA', 'Trade Signal']]
