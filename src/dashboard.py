import streamlit as st
from src.data_retrieval import get_stock_data
from src.visualization import create_candlestick_chart, create_sentiment_heatmap
from src.signal_generator import generate_signals
from src.sentiment_analysis import fetch_news, analyze_sentiment
from src.tools.moving_average import calculate_moving_average

def create_dashboard(debug_log):
    tabs = st.tabs([
        "📈 Price Analysis",
        "📊 Moving Averages",
        "🏢 Company Info",
        "📰 Sentiment Analysis",
        "💡 Trading Signals"
    ])

    # Price Analysis Tab
    with tabs[0]:
        symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL", key="symbol_price_analysis")
        if symbol:
            data = get_stock_data(symbol)
            if data is not None and not data.empty:
                st.plotly_chart(create_candlestick_chart(data, symbol), use_container_width=True)
            else:
                st.warning("Invalid stock symbol or no data available.")

    # Moving Averages Tab
    with tabs[1]:
        symbol = st.text_input("Enter stock symbol for Moving Averages:", "AAPL", key="symbol_moving_averages")
        days = st.slider("Select period for moving average (days):", 10, 200, value=50)
        if symbol:
            ma = calculate_moving_average(symbol, days)
            if ma:
                st.success(ma)
            else:
                st.warning("Not enough data to calculate the moving average.")

    # Sentiment Analysis Tab
    with tabs[3]:
        headlines = fetch_news(symbol)
        if headlines:
            sentiments = analyze_sentiment(headlines)
            st.plotly_chart(create_sentiment_heatmap(headlines, sentiments), use_container_width=True)
        else:
            st.warning("No news found for this symbol.")

    # Trading Signals Tab
    with tabs[4]:
        if symbol:
            signals = generate_signals(get_stock_data(symbol))
            if not signals.empty:
                st.dataframe(signals)
            else:
                st.warning("Not enough data to generate trading signals.")
