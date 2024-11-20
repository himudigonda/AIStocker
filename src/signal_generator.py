import pandas as pd

def generate_signals(data):
    if data is None or data.empty:
        return pd.DataFrame()

    data['Short_MA'] = data['Close'].rolling(window=10).mean()
    data['Long_MA'] = data['Close'].rolling(window=50).mean()

    # Ensure correct assignment using .loc
    data.loc[:, 'Signal'] = 0
    data.loc[data['Short_MA'] > data['Long_MA'], 'Signal'] = 1
    data.loc[data['Short_MA'] <= data['Long_MA'], 'Signal'] = -1

    data.loc[:, 'Trade Signal'] = data['Signal'].diff()
    return data[['Close', 'Short_MA', 'Long_MA', 'Trade Signal']]
