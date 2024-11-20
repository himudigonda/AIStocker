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
                if message["role"] == "assistant" and "detailed_thoughts" in message:
                    # Show a concise response by default with an option to expand
                    st.markdown(message["content"])  # Short response
                    with st.expander("See full detailed analysis"):
                        st.markdown(message["detailed_thoughts"])  # Full detailed analysis
                else:
                    st.markdown(message["content"])  # Default for user or short assistant responses

    def add_message(self, role, content, detailed_thoughts=None):
        """Add new message to the chat and update the session state."""
        self.logger.debug(f"[{role.upper()}] {content}")
        message = {"role": role, "content": content}
        if detailed_thoughts:
            message["detailed_thoughts"] = detailed_thoughts  # Store full analysis if available
        st.session_state.messages.append(message)
        with st.chat_message(role):
            st.markdown(content)  # Show short response in chat
            if detailed_thoughts:
                with st.expander("See full detailed analysis"):
                    st.markdown(detailed_thoughts)  # Option to expand full analysis

    def get_user_input(self):
        """Get input from the user and process it with the LLM handler."""
        user_input = st.chat_input("Ask Stocker something...")
        if user_input:
            # Add the user's input to the chat
            self.add_message("user", user_input)

            # Generate assistant's response (detailed + concise)
            dashboard_data = {
                "Price": "...",  # Latest price from dashboard
                "Company Info": get_company_info(self.active_symbol),
                "Sentiment": analyze_sentiment(fetch_news(self.active_symbol)),
            }
            response = self.llm_handler.process_query(user_input, dashboard_data)

            # Add LLM's concise and detailed response
            self.add_message("assistant", response['final_answer'], response['detailed_thoughts'])
