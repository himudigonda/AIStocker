import streamlit as st
from src.data_retrieval import get_stock_data
from src.visualization import create_candlestick_chart_with_ma
from src.tools.moving_average import calculate_moving_averages
from src.tools.company_info import get_company_info

def create_dashboard(debug_log):
    tabs = st.tabs([
        "📈 Price Analysis",
        "📊 Technical Indicators",
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
                ma_options = [5, 10, 20, 50, 100, 200]
                selected_ma = st.multiselect(
                    "Select Moving Averages to Display",
                    options=ma_options,
                    default=[10, 50]
                )
                for ma in selected_ma:
                    data[f"{ma}-Day MA"] = data['Close'].rolling(ma).mean()
                st.plotly_chart(create_candlestick_chart_with_ma(data, symbol, selected_ma))
            else:
                st.warning("Invalid stock symbol or no data available.")

    # Technical Indicators Tab (Improved Moving Averages)
    with tabs[1]:
        st.subheader("Technical Indicators")
        symbol = st.text_input("Enter stock symbol for Indicators:", "AAPL", key="symbol_tech_indicators")
        if symbol:
            data = get_stock_data(symbol)
            if data is not None:
                ma_options = [5, 10, 20, 50, 100, 200]
                selected_ma = st.multiselect(
                    "Select Moving Averages to Display",
                    options=ma_options,
                    default=[10, 50, 200]
                )
                for ma in selected_ma:
                    data[f"{ma}-Day MA"] = data['Close'].rolling(ma).mean()
                st.plotly_chart(create_candlestick_chart_with_ma(data, symbol, selected_ma))
            else:
                st.warning("Invalid stock symbol or no data available.")
