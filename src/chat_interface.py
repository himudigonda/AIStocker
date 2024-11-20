import streamlit as st

class ChatInterface:
    def __init__(self, logger, llm_handler, active_symbol):
        self.logger = logger
        self.llm_handler = llm_handler
        self.active_symbol = active_symbol

        # Initialize session state for chat messages
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def display(self):
        st.title("📈 AIStocker Chat Assistant")

        # Display chat messages from session state on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def add_message(self, role, content):
        """Add new message to the chat and update the session state."""
        self.logger.debug(f"[{role.upper()}] {content}")
        st.session_state.messages.append({"role": role, "content": content})
        with st.chat_message(role):
            st.markdown(content)

    def get_user_input(self):
        """Get input from the user and process it with the LLM handler."""
        user_input = st.chat_input("Ask Stocker something...")
        if user_input:
            # Add the user's input to the chat
            self.add_message("user", user_input)

            # Generate assistant's response
            response = self.llm_handler.process_query(user_input, self.active_symbol)

            # Add the assistant's response to the chat
            self.add_message("assistant", response)
