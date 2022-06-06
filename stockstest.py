"""Bill Casson - Portfolio Assignment

June 3, 2022

Test cases for the stocks module."""

import unittest
from datetime import date

from stocks import Stock, StockValue

class StockTest(unittest.TestCase):
    def setUp(self):
        """Create two stocks and two stock values to use for testing"""
        self.stock1 = Stock("GOOGL", "Alphabet Inc.", "https://www.google.com/", "Alphabet owns Google.", "cs")
        self.stock2 = Stock("AAPL", "Apple Inc.", "https://www.apple.com/", "Apple makes lots of stuff.", "cs")
        self.stock_value1 = StockValue(ticker="GOOGL", open_price=1, close_price=2, high=3, low=0, volume=100, timestamp=date.today())
        self.stock_value2 = StockValue("AAPL", open_price=4.5, close_price=3, high=5, low=1.2, volume=91, timestamp=date.today())

    def test_instance(self):
        """Test that the constructors worked and that the proper types exist"""
        self.assertIsInstance(self.stock1, Stock)
        self.assertIsInstance(self.stock2, Stock)
        self.assertIsInstance(self.stock_value1, StockValue)
        self.assertIsInstance(self.stock_value2, StockValue)
        
    def test_add_value(self):
        """Test that adding values to the values lists works"""
        self.stock1.add_value(self.stock_value1)
        self.assertIn(self.stock_value1, self.stock1.values)
        self.stock1.add_value(self.stock_value2)
        self.assertIn(self.stock_value1, self.stock1.values) # Ensure adding the second stock didn't remove the first one
        self.assertIn(self.stock_value2, self.stock1.values)

if __name__ == "__main__":
    unittest.main()
