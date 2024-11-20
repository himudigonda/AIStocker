from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LLMHandler:
    def __init__(self, logger):
        self.logger = logger

        # Load the Hugging Face model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("Xkev/Llama-3.2V-11B-cot")
        self.model = AutoModelForCausalLM.from_pretrained("Xkev/Llama-3.2V-11B-cot", device_map="auto")

        self.logger.debug("[DEBUG] LLMHandler initialized with Hugging Face model.")

    def process_query(self, query, symbol):
        """Generate a concise response to a user query."""
        # Context or prompt including stock symbol for LLM processing
        stock_context = f"User asked about stock: {symbol}. Question: {query}\n"

        inputs = self.tokenizer(stock_context, return_tensors="pt").to("cuda")
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=150,  # Keep responses short
            num_beams=3,  # Balanced decoding
            early_stopping=True
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Truncate to deliver only relevant output
        self.logger.debug(f"[DEBUG] LLM Raw Output: {response}")
        concise_response = self._truncate_response(response)
        return concise_response

    def _truncate_response(self, response):
        """Truncate the response to deliver concise answers."""
        # Heuristically trim long answers. Focus only on final insights.
        final_thoughts_start = response.rfind("Final Thoughts:")  # Look for analysis wrap-up
        if final_thoughts_start != -1:
            return response[final_thoughts_start + 15:].strip()
        return response[:300].strip()  # Default fallback to first 300 chars if no marker.
