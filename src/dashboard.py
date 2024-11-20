import streamlit as st
from src.data_retrieval import get_stock_data
from src.visualization import create_candlestick_chart_with_ma

def create_dashboard(logger):
    tabs = st.tabs([
        "📈 Price Analysis",
        "📊 Technical Indicators",
        "🏢 Company Info",
        "📰 Sentiment Analysis",
        "💡 Trading Signals"
    ])

    with tabs[0]:
        symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL", key="symbol_price_analysis")
        if symbol:
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
                    key=f"{symbol}_price_analysis_{selected_ma}"
                )
            else:
                st.warning("Invalid stock symbol or no data available.")
