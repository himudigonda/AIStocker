from langchain_experimental.llms.ollama_functions import OllamaFunctions
from tools.stock_price import get_stock_price, get_stock_price_schema
from tools.company_info import get_company_info, get_company_info_schema
from tools.moving_average import calculate_moving_average, calculate_moving_average_schema

class LLMHandler:
    def __init__(self):
        self.model = OllamaFunctions(model="llama3.1:latest", format="json")
        self.model = self.model.bind_tools(
            tools=[get_stock_price_schema, get_company_info_schema, calculate_moving_average_schema],
        )

    def process_query(self, query):
        response = self.model.invoke(query)
        if 'function_call' in response.additional_kwargs:
            function_name = response.additional_kwargs['function_call']['name']
            arguments = response.additional_kwargs['function_call']['arguments']

            if function_name == "get_stock_price":
                return get_stock_price(arguments['symbol'])
            elif function_name == "get_company_info":
                return get_company_info(arguments['symbol'])
            elif function_name == "calculate_moving_average":
                return calculate_moving_average(arguments['symbol'], arguments['days'])

        return response.content
