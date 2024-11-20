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
        # sentiment_summary = "\n".join([f"{headline}: {score:.2f}" for headline, score in dashboard_data['Sentiment']])
        sentiment_summary = "\n".join([f"{item['headline']}: {item['headline_sentiment']} | Content Sentiment: {item['content_sentiment']}"
        for item in dashboard_data['Sentiment']
        ])
        stock_data_context = f"""
        Symbol: {dashboard_data.get('Symbol')}
        Sentiment Analysis:
        {sentiment_summary}

        Company Info:
        {dashboard_data.get('Company Info')}

        Other Data:
        {dashboard_data}
        """
        response = self.chain.invoke({"question": query, "stock_data": stock_data_context})
        return self._split_response(response)

    def _process_with_huggingface(self, query, symbol):
        stock_context = f"User asked about stock: {symbol}. Question: {query}\n"
        inputs = self.tokenizer(stock_context, return_tensors="pt").to("cuda")
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=2000,  # Increased from 1000 to 2000
            num_beams=3,
            early_stopping=True,
            eos_token_id=self.tokenizer.eos_token_id,  # Ensure generation stops at end of sequence
            pad_token_id=self.tokenizer.pad_token_id
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self._split_response(response)

    def _split_response(self, response):
        """
        Split the response into detailed internal thoughts and a concise user-facing answer.
        """
        self.logger.debug(f"[DEBUG] LLM Full Analysis: {response}")

        # Assume response has sections for 'Analysis' and 'Conclusion'
        analysis_start = response.find("Analysis:")
        conclusion_start = response.find("Conclusion:")

        if analysis_start != -1 and conclusion_start != -1:
            detailed_thoughts = response[analysis_start:conclusion_start].strip()
            final_answer = response[conclusion_start:].strip()
        else:
            detailed_thoughts = response
            final_answer = response[:500].strip()  # Increased from 200 to 500 characters

        return {"detailed_thoughts": detailed_thoughts, "final_answer": final_answer}
