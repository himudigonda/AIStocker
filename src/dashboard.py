import streamlit as st
from src.data_retrieval import get_stock_data
from src.visualization import create_candlestick_chart
from src.signal_generator import generate_signals
from src.sentiment_analysis import fetch_news, analyze_sentiment

def create_dashboard(debug_log):
    tabs = st.tabs(["Price Analysis", "Moving Averages", "Company Info", "Sentiment Analysis", "Trading Signals"])

    # Tab 1: Price Analysis
    with tabs[0]:
        symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL")
        if symbol:
            debug_log.write(f"[DEBUG] Fetching data for symbol: {symbol}")
            data = get_stock_data(symbol)
            if data is not None:
                fig = create_candlestick_chart(data, symbol)
                st.plotly_chart(fig, use_container_width=True)
                st.success(f"Data loaded successfully for {symbol}. Analysis started.")
            else:
                st.warning("Failed to retrieve data. Please check the symbol.")

    # Tab 2: Moving Averages
    with tabs[1]:
        st.subheader("Moving Averages")
        if data is not None:
            st.write("Calculating moving averages...")
            # Placeholder: add moving average plots or summaries

    # Tab 3: Company Info
    with tabs[2]:
        st.subheader("Company Information")
        # Placeholder to fetch company details and show them

    # Tab 4: Sentiment Analysis
    with tabs[3]:
        st.subheader("Sentiment Analysis")
        headlines = fetch_news(symbol)
        if headlines:
            sentiments = analyze_sentiment(headlines)
            st.write("Top News & Sentiments")
            for headline, sentiment in zip(headlines, sentiments):
                st.write(f"{headline} - Sentiment Score: {sentiment}")
        else:
            st.warning("No recent news available for this symbol.")

    # Tab 5: Trading Signals
    with tabs[4]:
        st.subheader("Trading Signals")
        if data is not None:
            signals = generate_signals(data)
            st.write(signals)
