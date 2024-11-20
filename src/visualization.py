import plotly.graph_objs as go
import plotly.express as px

def create_candlestick_chart_with_ma(data, symbol, short_ma=None, long_ma=None):
    fig = go.Figure()

    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=f"{symbol} Price"
    ))

    # Add short-term moving average
    if short_ma is not None:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[short_ma],
            mode='lines',
            line=dict(color='blue', width=1.5),
            name=f"{short_ma}-Day MA"
        ))

    # Add long-term moving average
    if long_ma is not None:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[long_ma],
            mode='lines',
            line=dict(color='orange', width=1.5),
            name=f"{long_ma}-Day MA"
        ))

    fig.update_layout(
        title=f"{symbol} Stock Price with Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )

    return fig
