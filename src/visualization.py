import plotly.graph_objs as go
import plotly.express as px

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
    fig.update_layout(
        title=f"{symbol} Stock Price Analysis",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )
    return fig

def create_sentiment_heatmap(headlines, sentiments):
    df = {"Headline": headlines, "Sentiment": sentiments}
    fig = px.bar(df, x="Headline", y="Sentiment", color="Sentiment", text_auto=True)
    fig.update_layout(template="plotly_dark", title="Sentiment Heatmap")
    return fig
