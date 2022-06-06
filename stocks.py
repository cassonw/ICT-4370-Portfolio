"""Bill Casson - Portfolio Assignment

June 3, 2022

This module contains classes for representing stock info and values."""

class Stock:
    def __init__(self, ticker, name, homepage, description, type):
        """Initialize the stock with the ticker, ticker details, and create an empty list to hold stock values for each day."""
        self.ticker = ticker
        self.name = name
        self.homepage = homepage
        self.description = description
        self.type = type
        self.values = []

    def add_value(self, value):
        """Add the provided value to the list of values"""
        self.values.append(value)

class StockValue:
    def __init__(self, ticker, open_price, close_price, high, low, volume, timestamp):
        """IInitialize the values of each of the parameters in the object. open_price, close_price, high, low, and volume represent the information for the given ticker on the timestamp date."""
        self.ticker = ticker
        self.open_price = open_price
        self.close_price = close_price
        self.high = high
        self.low = low
        self.volume = volume
        self.timestamp = timestamp
