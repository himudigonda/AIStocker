def generate_signals(data):
    """
    Generates buy/sell signals based on moving averages.

    Args:
        data (pd.DataFrame): DataFrame with stock price data including moving averages.

    Returns:
        List of signals.
    """
    signals = []
    data['Signal'] = 0
    data['Signal'][data['Short_MA'] > data['Long_MA']] = 1
    data['Signal'][data['Short_MA'] <= data['Long_MA']] = -1

    signals = data['Signal'].diff()
    return signals
