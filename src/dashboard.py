from src.signal_generator import generate_signals
import streamlit as st
from src.data_retrieval import get_stock_data
from src.visualization import create_candlestick_chart_with_ma
from src.sentiment_analysis import fetch_news, analyze_sentiment
from src.tools.company_info import get_company_info

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
        data = get_stock_data(symbol)
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
        data = get_stock_data(symbol)
        if data is not None:
            ma_options = [5, 10, 20, 50, 100, 200]
            selected_ma = st.multiselect(
                "Select Moving Averages to Display",
                options=ma_options,
                default=[10, 50]
            )
            for ma in selected_ma:
                data[f"{ma}-Day MA"] = data['Close'].rolling(ma).mean()
            st.plotly_chart(
                create_candlestick_chart_with_ma(data, symbol, selected_ma),
                use_container_width=True,
                key=f"{symbol}_technical_indicators_{selected_ma}"
            )
        else:
            st.warning("Invalid stock symbol or no data available.")

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
        headlines = fetch_news(symbol)

        if headlines:
            st.write(f"**Recent news for {symbol}:**")

            sentiments = analyze_sentiment([h[0] for h in headlines])  # Analyze sentiment for all headlines
            sentiment_labels = ['Negative', 'Neutral', 'Positive']
            sentiment_thresholds = [-0.1, 0.1]  # Define thresholds for sentiment classification

            for i, (headline, link, pub_date) in enumerate(headlines):
                sentiment = sentiments[i]
                if sentiment < sentiment_thresholds[0]:
                    sentiment_text = sentiment_labels[0]  # Negative
                elif sentiment > sentiment_thresholds[1]:
                    sentiment_text = sentiment_labels[2]  # Positive
                else:
                    sentiment_text = sentiment_labels[1]  # Neutral

                st.markdown(f"**[{headline}]({link})**  \nPublished on: {pub_date}  \nSentiment: **{sentiment_text}** ({sentiment:.2f})")

            # Calculate overall sentiment score
            overall_sentiment = sum(sentiments) / len(sentiments)
            if overall_sentiment < sentiment_thresholds[0]:
                overall_sentiment_text = sentiment_labels[0]  # Negative
            elif overall_sentiment > sentiment_thresholds[1]:
                overall_sentiment_text = sentiment_labels[2]  # Positive
            else:
                overall_sentiment_text = sentiment_labels[1]  # Neutral

            st.write(f"**Overall Sentiment:** {overall_sentiment_text} ({overall_sentiment:.2f})")

        else:
            st.warning("No recent news available.")


    # Trading Signals Tab
    with tabs[4]:
        st.subheader("💡 Trading Signals")
        symbol = st.session_state.symbol
        data = get_stock_data(symbol)

        if data is not None:
            signals = generate_signals(data)
            if not signals.empty:
                st.write("Recent Trading Signals:")
                st.dataframe(signals.tail(10), use_container_width=True)

                # Add a chart for MACD and Bollinger Bands
                st.write("Technical Indicators Visualized:")
                st.line_chart(data[['MACD', 'Signal_Line', 'Upper_Band', 'Lower_Band']].tail(50))
            else:
                st.warning("No signals generated. Ensure data is sufficient.")
        else:
            st.warning("Invalid stock symbol or no data available.")
