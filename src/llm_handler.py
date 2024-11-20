from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from src.tools import get_stock_price, get_company_info, calculate_moving_averages
from src.data_retrieval import get_stock_data
from src.sentiment_analysis import fetch_news, analyze_sentiment

class LLMHandler:
    def __init__(self, logger):
        self.logger = logger

        # Initialize model and prompt
        self.prompt = ChatPromptTemplate.from_template("""
        Question: {question}

        Stock Data Context:
        {stock_data}

        Answer: Let's think step by step based on the available data and analysis.
        """)
        self.model = OllamaLLM(model="llama3.1:latest")
        self.chain = self.prompt | self.model

        self.logger.debug("[DEBUG] LLMHandler initialized with tools and model.")

    def fetch_contextual_data(self, symbol):
        """Fetch all relevant data for the given stock symbol."""
        try:
            stock_data = get_stock_data(symbol)
            ma_10 = stock_data['Close'].rolling(10).mean().iloc[-1]
            ma_50 = stock_data['Close'].rolling(50).mean().iloc[-1]
            company_info = get_company_info(symbol)
            news = fetch_news(symbol)
            sentiments = analyze_sentiment(news)

            context = f"""
            Symbol: {symbol}
            Current Price: {get_stock_price(symbol)}
            10-Day MA: ${ma_10:.2f}
            50-Day MA: ${ma_50:.2f}
            Company Info: {company_info.get('Company Name', 'N/A')} | {company_info.get('Industry', 'N/A')} | {company_info.get('Sector', 'N/A')}
            Recent News: {', '.join(news[:3]) if news else 'No recent news found.'}
            Sentiment Scores: {sentiments[:3] if sentiments else 'No sentiment data.'}
            """
            return context
        except Exception as e:
            self.logger.error(f"[ERROR] Fetching contextual data failed: {e}")
            return "Unable to fetch complete context."

    def process_query(self, query, symbol):
        """Process user query and include dashboard context."""
        self.logger.debug(f"[DEBUG] Processing query: {query} with symbol: {symbol}")
        stock_data = self.fetch_contextual_data(symbol)
        response = self.chain.invoke({"question": query, "stock_data": stock_data})

        if isinstance(response, str):
            return response
        else:
            return "Unable to process the query at the moment."
