import plotly.graph_objs as go

def create_candlestick_chart_with_ma(data, symbol, selected_ma):
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

    # Add selected moving averages
    for ma in selected_ma:
        ma_column = f"{ma}-Day MA"
        if ma_column in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data[ma_column],
                mode='lines',
                line=dict(width=1.5),
                name=f"{ma}-Day MA"
            ))

    fig.update_layout(
        title=f"{symbol} Stock Price with Selected Indicators",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis=dict(
            fixedrange=False,  # This allows vertical zooming
            type="linear"
        ),
        dragmode='zoom',  # This enables both vertical and horizontal zooming
        showlegend=True
    )

    return fig
