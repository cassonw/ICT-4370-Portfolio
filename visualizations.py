'''Bill Casson - Week 8 Assignment
May 19, 2022

This program will read in stock  and stock value information and display the performance of those stocks over time.'''

import sqlite3
from datetime import datetime
from operator import itemgetter

import matplotlib.pyplot as plt

from stocks import Stock, StockValue

tickers = ["GOOGL", "AAPL", "MSFT", "AMZN", "TSLA"] # The top 5 companies in the U.S. by market cap on June 3, 2022

# create a connection to the database and retreive a cursor object
con = sqlite3.connect("stock_info.db")
cursor = con.cursor()

# Fetch all of the ticker details from the database for the tickers in 'tickers.'
sql = "select ticker, name, homepage, description, type FROM stocks where ticker in ("

for ticker in tickers:
    sql += f'"{ticker}", '
sql = sql[:-2] + ");" # Remove the last ', ' from the string and append the closing ');'.
cursor.execute(sql)
stocks = {}
for ticker_details in cursor.fetchall():
    stocks[ticker_details[0]] = Stock(*ticker_details)

# Read in all the stock values from the database
for ticker, stock in stocks.items():
    cursor.execute(f"select ticker, open, close, high, low, volume, timestamp from stock_values where ticker = '{ticker}'")
    for ticker_value in cursor.fetchall():
        stock.add_value(StockValue(*ticker_value))

# Create the graph and add all the stocks to it.
fig, ax = plt.subplots()
for stock in stocks.values():
    dates = [datetime.fromtimestamp(stock_value.timestamp).date() for stock_value in stock.values]
    values = [stock_value.close_price for stock_value in stock.values]
    ax.plot(dates, values, label=f"{stock.name} ({stock.ticker})")
ax.set_xlabel("Date")
ax.set_ylabel("Stock Value")
ax.set_title("Top 5 company's stock Performance")
ax.legend()
plt.savefig("stock_values.png")
