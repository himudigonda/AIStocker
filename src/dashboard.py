import streamlit as st
from src.data_retrieval import get_stock_data
from src.visualization import create_candlestick_chart_with_ma
from src.signal_generator import generate_signals
from src.sentiment_analysis import fetch_news, analyze_sentiment
from src.tools.moving_average import calculate_moving_average
from src.tools.company_info import get_company_info

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
            if data is not None:
                ma_10 = data['Close'].rolling(10).mean()
                ma_50 = data['Close'].rolling(50).mean()
                data['10-Day MA'] = ma_10
                data['50-Day MA'] = ma_50
                st.plotly_chart(create_candlestick_chart_with_ma(data, symbol, '10-Day MA', '50-Day MA'))

    # Company Info Tab
    with tabs[2]:
        symbol = st.text_input("Enter company symbol:", "AAPL", key="symbol_company_info")
        if symbol:
            info = get_company_info(symbol)
            if "Error" in info:
                st.warning(info["Error"])
            else:
                st.subheader(f"{info['Company Name']}")
                st.write(f"**Industry**: {info['Industry']}")
                st.write(f"**Sector**: {info['Sector']}")
                st.write(f"**Business Summary**: {info['Business Summary']}")
