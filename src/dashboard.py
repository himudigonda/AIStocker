import streamlit as st
from src.tools.company_info import get_company_info, interpret_company_metrics
from src.sentiment_analysis import fetch_news
from src.visualization import create_candlestick_chart_with_ma
from src.data_retrieval import get_stock_data

def create_dashboard(logger):
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
        symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL", key="symbol_price_analysis")
        if symbol:
            data = get_stock_data(symbol)
            if data is not None:
                st.plotly_chart(create_candlestick_chart_with_ma(data, symbol, []), use_container_width=True)
            else:
                st.warning("No stock data found.")

    # Technical Indicators Tab
    with tabs[1]:
        st.subheader("📊 Technical Indicators")
        symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL", key="symbol_technical_indicators")
        if symbol:
            data = get_stock_data(symbol)
            if data is not None:
                ma_options = [10, 50, 100]
                selected_ma = st.multiselect("Select Moving Averages", ma_options, default=[10, 50])
                for ma in selected_ma:
                    data[f"{ma}-Day MA"] = data['Close'].rolling(ma).mean()
                st.plotly_chart(create_candlestick_chart_with_ma(data, symbol, selected_ma), use_container_width=True)
            else:
                st.warning("No stock data found.")

    # Company Info Tab
    with tabs[2]:
        st.subheader("🏢 Company Info")
        symbol = st.text_input("Enter stock symbol:", "AAPL", key="symbol_company_info")
        if symbol:
            company_info = get_company_info(symbol)
            if company_info:
                st.write(f"**Company Name:** {company_info['Company Name']}")
                st.write(f"**Sector:** {company_info['Sector']}")
                st.write(f"**Industry:** {company_info['Industry']}")
                st.write(f"**Business Summary:** {company_info['Business Summary']}")
                st.write(f"**Market Cap:** {company_info['Market Cap']}")
                st.write(f"**Revenue:** {company_info['Revenue']}")
                st.write(f"**Net Income:** {company_info['Net Income']}")
                st.write(f"**EPS:** {company_info['EPS']}")
                st.write(f"**P/E Ratio:** {company_info['P/E Ratio']}")
                st.write(f"**Dividend Yield:** {company_info['Dividend Yield']}")
                st.write(f"**ROE:** {company_info['ROE']}")
                st.write(f"**ROA:** {company_info['ROA']}")
                st.write(f"**Debt-to-Equity:** {company_info['Debt-to-Equity']}")
                st.markdown(f"[View Latest Annual Report (10-K)]({company_info['Annual Report']})")
                investment_insights = interpret_company_metrics(company_info)
                if investment_insights:
                    st.write("### Investment Insights:")
                    for insight in investment_insights:
                        st.write(f"- {insight}")
            else:
                st.warning("No company information found.")
    # Sentiment Analysis Tab
    with tabs[3]:
        st.subheader("📰 Sentiment Analysis")
        symbol = st.text_input("Enter stock symbol for sentiment analysis:", "AAPL", key="symbol_sentiment")
        if symbol:
            news = fetch_news(symbol)
            if news:
                overall_sentiment = 0
                for i, item in enumerate(news):
                    st.markdown(f"**{i+1}. [{item['headline']}]({item['link']})**")
                    st.write(f"Published on: {item['date']}")
                    st.write(f"Sentiment Score: {item['sentiment']}")
                    overall_sentiment += item['sentiment']
                avg_sentiment = overall_sentiment / len(news)
                st.write(f"**Overall Sentiment Score:** {avg_sentiment:.2f}")
            else:
                st.warning("No recent news articles found.")
