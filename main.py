import streamlit as st
from src.chat_interface import ChatInterface
from src.dashboard import create_dashboard
from src.llm_handler import LLMHandler

def main():
    st.set_page_config(page_title="AIStocker", layout="wide", initial_sidebar_state="collapsed")
    st.title("AIStocker: Intelligent Stock Analysis Chatbot")

    col1, col2 = st.columns([1, 2])

    debug_log = st.expander("Debug Log", expanded=True)
    chat_interface = ChatInterface(debug_log)
    llm_handler = LLMHandler(debug_log)

    with col1:
        chat_interface.display()
        user_input = chat_interface.get_user_input()
        if user_input:
            chat_interface.add_message("user", user_input)
            response = llm_handler.process_query(user_input)
            chat_interface.add_message("assistant", response)

    with col2:
        st.header("Dashboard")
        create_dashboard(debug_log)

if __name__ == "__main__":
    main()
