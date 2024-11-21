from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class LLMHandler:
    def __init__(self, logger, selected_model="Ollama (Default)"):
        self.logger = logger
        self.selected_model = selected_model
        self._initialize_model()

    def _initialize_model(self):
        if self.selected_model == "Ollama (Default)":
            self.logger.debug("[DEBUG] Initializing Ollama model.")
            self.prompt = ChatPromptTemplate.from_template("""
                Question: {question}

                Stock Data Context:
                {stock_data}

                Answer: Let's analyze step by step and generate concise insights.
                ---
                Detailed Analysis:
                [Provide a detailed breakdown of the data and insights, step by step.]

                Final Answer:
                [Provide a short, actionable summary or conclusion based on the analysis above.]
            """)
            self.model = OllamaLLM(model="llama3.1:latest")
            self.chain = self.prompt | self.model
        elif self.selected_model == "HuggingFace (Xkev/Llama-3.2V-11B-cot)":
            self.logger.debug("[DEBUG] Initializing Hugging Face model.")
            self.tokenizer = AutoTokenizer.from_pretrained("Xkev/Llama-3.2V-11B-cot")
            self.model = AutoModelForCausalLM.from_pretrained("Xkev/Llama-3.2V-11B-cot", device_map="auto")

    def process_query(self, query, dashboard_data):
        if self.selected_model == "Ollama (Default)":
            return self._process_with_ollama(query, dashboard_data)
        elif self.selected_model == "HuggingFace (Xkev/Llama-3.2V-11B-cot)":
            return self._process_with_huggingface(query, dashboard_data)

    def _process_with_ollama(self, query, dashboard_data):
        # Prepare sentiment summary
        sentiment_summary = "\n".join([
            f"{item['headline']}: {item['headline_sentiment']} | Content Sentiment: {item['content_sentiment']}"
            for item in dashboard_data.get('Sentiment', [])
        ])

        # Prepare stock data context
        stock_data_context = f"""
        Symbol: {dashboard_data.get('Symbol', 'N/A')}
        Sentiment Analysis:
        {sentiment_summary}

        Company Info:
        {dashboard_data.get('Company Info', 'N/A')}

        Other Data:
        {dashboard_data}
        """
        # Invoke Ollama model
        response = self.chain.invoke({"question": query, "stock_data": stock_data_context})
        return self._split_response(response)

    def _process_with_huggingface(self, query, dashboard_data):
        # Prepare stock context for HuggingFace model
        sentiment_summary = "\n".join([
            f"{item['headline']}: {item['headline_sentiment']} | Content Sentiment: {item['content_sentiment']}"
            for item in dashboard_data.get('Sentiment', [])
        ])

        stock_context = f"""
        User asked: {query}

        Stock Data Context:
        Symbol: {dashboard_data.get('Symbol', 'N/A')}
        Sentiment Analysis:
        {sentiment_summary}

        Company Info:
        {dashboard_data.get('Company Info', 'N/A')}
        """
        # Generate response using HuggingFace model
        inputs = self.tokenizer(stock_context, return_tensors="pt").to("cuda")
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=2000,
            num_beams=3,
            early_stopping=True,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self._split_response(response)

    def _split_response(self, response):
        """
        Split the response into detailed internal thoughts and a concise user-facing answer.
        """
        self.logger.debug(f"[DEBUG] LLM Full Analysis: {response}")

        # Assume response has sections for 'Detailed Analysis' and 'Final Answer'
        analysis_start = response.find("Detailed Analysis:")
        final_answer_start = response.find("Final Answer:")

        if analysis_start != -1 and final_answer_start != -1:
            detailed_thoughts = response[analysis_start + len("Detailed Analysis:"):final_answer_start].strip()
            final_answer = response[final_answer_start + len("Final Answer:"):].strip()
        else:
            # Fallback: If structure is not as expected
            detailed_thoughts = response.strip()
            final_answer = response[:300].strip()  # Take the first 300 characters for a concise response

        return {"detailed_thoughts": detailed_thoughts, "final_answer": final_answer}
