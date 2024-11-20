import streamlit as st

class ChatInterface:
    def __init__(self, logger, llm_handler, active_symbol):
        self.logger = logger
        self.llm_handler = llm_handler
        self.active_symbol = active_symbol
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def display(self):
        st.title("📈 AIStocker Chat Assistant")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def add_message(self, role, content):
        self.logger.debug(f"[{role.upper()}] {content}")
        st.session_state.messages.append({"role": role, "content": content})
        with st.chat_message(role):
            st.markdown(content)

    def get_user_input(self):
        user_input = st.chat_input("Ask Stocker.")
        if user_input:
            self.add_message("user", user_input)
            response = self.llm_handler.process_query(user_input, self.active_symbol)
            self.add_message("assistant", response)
