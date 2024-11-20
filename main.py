import streamlit as st
from src.chat_interface import ChatInterface
from src.dashboard import create_dashboard
from src.llm_handler import LLMHandler

def main():
    st.set_page_config(page_title="📈 AIStocker", layout="wide", initial_sidebar_state="collapsed")

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("# 📈 AIStocker")
        st.radio(
            "Dashboard Sections",
            options=["Price Analysis", "Technical Indicators", "Company Info", "Sentiment Analysis", "Trading Signals"],
            key="dashboard_section"
        )
        st.text_input("Quick Stock Search", placeholder="Enter stock symbol (e.g., AAPL)", key="quick_search")

    # Debug & Content
    debug_log = st.expander("Debug Log", expanded=True)
    llm_handler = LLMHandler(debug_log)

    create_dashboard(debug_log)

if __name__ == "__main__":
    main()
