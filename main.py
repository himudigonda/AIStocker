import streamlit as st
import logging
from src.chat_interface import ChatInterface
from src.dashboard import create_dashboard
from src.llm_handler import LLMHandler

# Configure logging for terminal output
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        active_symbol = st.text_input("Quick Stock Search", placeholder="Enter stock symbol (e.g., AAPL)", key="quick_search", value="AAPL")

    # Initialize LLMHandler with logger
    llm_handler = LLMHandler(logger)

    # Chat Interface
    col1, col2 = st.columns([1, 2], gap="small")

    # Left column: Chat interface
    with col1:
        chat_interface = ChatInterface(logger, llm_handler, active_symbol)
        chat_interface.display()
        chat_interface.get_user_input()

    # Right column: Dashboard
    with col2:
        create_dashboard(logger)

if __name__ == "__main__":
    main()
