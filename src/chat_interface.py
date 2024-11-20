import streamlit as st

class ChatInterface:
    def __init__(self, debug_log):
        self.debug_log = debug_log
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def display(self):
        st.title("Stock Market Analysis Chatbot")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def add_message(self, role, content):
        self.debug_log.write(f"[DEBUG] {role} message: {content}")
        st.session_state.messages.append({"role": role, "content": content})
        with st.chat_message(role):
            st.markdown(content)

    def get_user_input(self):
        return st.chat_input("Ask about stock analysis, technical metrics, or general financial advice.")
