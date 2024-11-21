import streamlit as st
from src.signal_generator import generate_signals
from src.data_retrieval import get_stock_data
from src.visualization import create_candlestick_chart_with_ma
from src.sentiment_analysis import fetch_news, analyze_sentiment
from src.tools.company_info import get_company_info
from textblob import TextBlob

def create_dashboard(logger):
    # Ensure the symbol persists across tabs
    if "symbol" not in st.session_state:
        st.session_state["symbol"] = "AAPL"  # Default stock symbol

    # Create input once, outside the tabs, to keep it persistent
    st.text_input("Enter stock symbol (e.g., AAPL):", st.session_state["symbol"], key="symbol_input", on_change=lambda: st.session_state.update({"symbol": st.session_state.symbol_input}))

    tabs = st.tabs([
        "📈 Price Analysis",
        "📊 Technical Indicators",
        "🏢 Company Info",
        "📰 Sentiment Analysis",
        "💡 Trading Signals"
    ])

    # Price Analysis Tab
    with tabs[0]:
        st.subheader("📈 Price Analysis")
        symbol = st.session_state.symbol
        max_period = "1y"
        duration = "1d"
        data = get_stock_data(symbol, period=max_period, interval=duration)
        if data is not None:
            st.plotly_chart(
                create_candlestick_chart_with_ma(data, symbol, []),  # No moving averages in Price Analysis
                use_container_width=True,
                key=f"{symbol}_price_analysis"
            )
        else:
            st.warning("Invalid stock symbol or no data available.")

    # Technical Indicators Tab
    with tabs[1]:
        st.subheader("📊 Technical Indicators")
        symbol = st.session_state.symbol

        # Add a radio button for interval selection
        duration = st.radio(
            "Candlestick Duration",
            options=["1d", "1wk", "1mo"],  # Only valid intervals
            index=0,  # Default to "1d"
            horizontal=True
        )

        # Set the period to fetch up to 8 years of data
        max_period = "1y"  # Fetch 8 years of data

        # Attempt to fetch data
        data = get_stock_data(symbol, period=max_period, interval=duration)

        if data is not None and not data.empty:
            st.write("Select the technical indicators you want to display:")

            # Use st.columns to arrange checkboxes horizontally
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                show_5_day_ma = st.checkbox("5-Day MA", value=False)
            with col2:
                show_10_day_ma = st.checkbox("10-Day MA", value=True)
            with col3:
                show_20_day_ma = st.checkbox("20-Day MA", value=False)
            with col4:
                show_50_day_ma = st.checkbox("50-Day MA", value=True)
            with col5:
                show_100_day_ma = st.checkbox("100-Day MA", value=False)
            with col6:
                show_200_day_ma = st.checkbox("200-Day MA", value=False)

            # Determine which moving averages are selected
            selected_ma = []
            if show_5_day_ma:
                selected_ma.append(5)
            if show_10_day_ma:
                selected_ma.append(10)
            if show_20_day_ma:
                selected_ma.append(20)
            if show_50_day_ma:
                selected_ma.append(50)
            if show_100_day_ma:
                selected_ma.append(100)
            if show_200_day_ma:
                selected_ma.append(200)

            # Add selected moving averages to the data
            for ma in selected_ma:
                data[f"{ma}-Day MA"] = data['Close'].rolling(ma).mean()

            # Display the candlestick chart with selected indicators
            st.plotly_chart(
                create_candlestick_chart_with_ma(data, symbol, selected_ma),
                use_container_width=True,
                key=f"{symbol}_technical_indicators_{selected_ma}_{duration}"
            )
        else:
            st.error("Failed to retrieve data. Please check the stock symbol.")
    # Company Info Tab
    with tabs[2]:
        st.subheader("🏢 Company Info")
        symbol = st.session_state.symbol
        company_info = get_company_info(symbol)
        if "Error" not in company_info:
            for key, value in company_info.items():
                st.write(f"**{key}:** {value}")
        else:
            st.warning("Could not fetch company information.")

    # Sentiment Analysis Tab
    with tabs[3]:
        st.subheader("📰 Sentiment Analysis")
        symbol = st.session_state.symbol
        articles = fetch_news(symbol)

        if articles:
            st.write(f"**Recent news for {symbol}:**")

            # Perform sentiment analysis on articles
            sentiment_results = analyze_sentiment(articles)

            for article in sentiment_results:
                st.markdown(f"### [{article['headline']}]({article['link']})")
                st.write(f"**Published on:** {article['pub_date']}")
                st.write(f"**Headline Sentiment:** {article['headline_sentiment']}")
                st.write(f"**Content Sentiment:** {article['content_sentiment']}")

                # Display summary in an expandable box
                with st.expander("Summary of the Article"):
                    st.write(article["summary"])
        else:
            st.warning("No recent news available.")

    with tabs[4]:
        st.subheader("💡 Trading Signals")
        symbol = st.session_state.symbol

        # Fetch stock data
        st.write(f"Fetching data for symbol: {symbol}")
        data = get_stock_data(symbol, period="1y", interval="1d")  # Long history and daily interval
        print(">?>data:  ",data)
        if data is not None:
            st.write("Generating trading signals...")
            signals = generate_signals(data)

            if not signals.empty:
                st.write("Recent Trading Signals:")
                st.dataframe(signals.tail(10), use_container_width=True)

                # Add visualization for MACD and Bollinger Bands
                st.write("Technical Indicators Visualized:")
                st.line_chart(data[['MACD', 'Signal_Line', 'Upper_Band', 'Lower_Band']].tail(50))
            else:
                st.warning("No trading signals generated. Ensure data is sufficient.")
        else:
            st.error(f"Invalid stock symbol ({symbol}) or no data available. Please check and try again.")
