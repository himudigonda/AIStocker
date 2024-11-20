import plotly.graph_objs as go

def create_candlestick_chart(data, symbol):
    fig = go.Figure(
        data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )]
    )
    fig.update_layout(title=f"{symbol} Stock Price Analysis", xaxis_title='Date')
    return fig
