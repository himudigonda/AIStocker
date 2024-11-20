import unittest
from src.tools.stock_price import get_stock_price
from src.tools.company_info import get_company_info
from src.tools.moving_average import calculate_moving_average

class TestTools(unittest.TestCase):
    def test_get_stock_price(self):
        result = get_stock_price("AAPL")
        self.assertIn("AAPL", result)
        self.assertIn("$", result)

    def test_get_company_info(self):
        result = get_company_info("AAPL")
        self.assertIn("Apple", result)
        self.assertIn("company", result)

    def test_calculate_moving_average(self):
        result = calculate_moving_average("AAPL", 50)
        self.assertIn("50-day moving average", result)
        self.assertIn("AAPL", result)
        self.assertIn("$", result)

if __name__ == '__main__':
    unittest.main()
