import streamlit as st
import plotly.graph_objs as go
from src.data_retrieval import get_stock_data
from src.visualization import create_candlestick_chart

def create_dashboard(debug_log):
    tabs = st.tabs(["Price Analysis", "Moving Averages", "Company Info"])

    with tabs[0]:
        symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL")
        if symbol:
            debug_log.write(f"[DEBUG] Fetching data for symbol: {symbol}")
            data = get_stock_data(symbol)
            if data is not None:
                fig = create_candlestick_chart(data, symbol)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Failed to retrieve data. Please check the symbol.")
