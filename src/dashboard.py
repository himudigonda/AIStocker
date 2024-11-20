import streamlit as st
import plotly.graph_objs as go
from data_retrieval import get_stock_data

def create_dashboard():
    st.title("Stock Market Dashboard")
    symbol = st.text_input("Enter a stock symbol:", value="AAPL")
    if symbol:
        data = get_stock_data(symbol)
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'])])
        fig.update_layout(title=f"{symbol} Stock Price")
        st.plotly_chart(fig)
