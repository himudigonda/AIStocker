import unittest
from src.llm_handler import LLMHandler

class TestLLMHandler(unittest.TestCase):
    def setUp(self):
        self.llm_handler = LLMHandler()

    def test_process_query(self):
        query = "What's the current stock price of Apple?"
        result = self.llm_handler.process_query(query)
        self.assertIn("AAPL", result)
        self.assertIn("$", result)

if __name__ == '__main__':
    unittest.main()
