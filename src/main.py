import streamlit as st
from chat_interface import ChatInterface
from dashboard import create_dashboard
from llm_handler import LLMHandler

def main():
    st.set_page_config(layout="wide")

    chat_interface = ChatInterface()
    llm_handler = LLMHandler()

    col1, col2 = st.columns([1, 1])

    with col1:
        chat_interface.display()
        user_input = st.text_input("Enter your stock market query:")
        if user_input:
            response = llm_handler.process_query(user_input)
            st.write(response)

    with col2:
        create_dashboard()

if __name__ == "__main__":
    main()
