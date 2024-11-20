from langchain_core.prompts import ChatPromptTemplate
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

    def process_query(self, query, symbol):
        if self.selected_model == "Ollama (Default)":
            return self._process_with_ollama(query, symbol)
        elif self.selected_model == "HuggingFace (Xkev/Llama-3.2V-11B-cot)":
            return self._process_with_huggingface(query, symbol)

    def _process_with_ollama(self, query, symbol):
        stock_data = f"Symbol: {symbol}, Question: {query}"
        response = self.chain.invoke({"question": query, "stock_data": stock_data})
        return self._split_response(response)

    def _process_with_huggingface(self, query, symbol):
        stock_context = f"User asked about stock: {symbol}. Question: {query}\n"
        inputs = self.tokenizer(stock_context, return_tensors="pt").to("cuda")
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=300,
            num_beams=3,
            early_stopping=True
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self._split_response(response)

    def _split_response(self, response):
        """
        Split the response into detailed internal thoughts and a concise user-facing answer.
        """
        self.logger.debug(f"[DEBUG] LLM Full Analysis: {response}")

        # Use simple keyword parsing to identify sections. Assume response has sections for 'Analysis' and 'Conclusion'
        analysis_start = response.find("Analysis:")
        conclusion_start = response.find("Conclusion:")

        if analysis_start != -1 and conclusion_start != -1:
            detailed_thoughts = response[analysis_start:conclusion_start].strip()
            final_answer = response[conclusion_start + 11:].strip()
        else:
            detailed_thoughts = response
            final_answer = "Here are my thoughts: " + response[:150].strip()  # Default concise reply if no clear conclusion.

        return {"detailed_thoughts": detailed_thoughts, "final_answer": final_answer}
