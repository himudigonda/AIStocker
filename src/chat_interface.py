import streamlit as st

class ChatInterface:
    def __init__(self):
        self.messages = []

    def display(self):
        st.title("Stock Market Analysis Chatbot")
        for message in self.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
