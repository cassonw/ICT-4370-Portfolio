'''Bill Casson - Week 10 Assignment
June 3,2022

This program will create the stock value table in the database and populate it with the stock values.'''

import datetime
import sqlite3
import sys
import time

from polygon import RESTClient

# The API key for the Polygon service.
POLYGON_API_KEY = "OErR5cSwTOYw5FJjaQ2zpjppV7K3dWCN"
tickers = ["GOOGL", "AAPL", "MSFT", "AMZN", "TSLA"] # The top 5 companies in the U.S. by market cap on June 3, 2022

# Create a connection to the SQLite database file
con = sqlite3.connect("stock_info.db")
cursor = con.cursor()

# Create the client for making the API requests.
client = RESTClient(POLYGON_API_KEY)

# Create the stock table
sql = """CREATE TABLE if not exists stocks (
    stock_id INTEGER PRIMARY KEY,
    ticker text not null,
    name text not null,
    homepage text,
    description text,
    type text
    )"""
cursor.execute(    sql)

# Insert the ticker details in the stocks table.
def insert_stocks_into_table(stock_details):
    """Insert the information from the polygon.rest.models.TickerDetails object into the stocks table."""
    sql = """insert into stocks 
        (ticker, name, homepage, description, type) 
        values """
    sql += f'("{stock_details.ticker}", "{stock_details.name}", "{stock_details.homepage_url}", "{stock_details.description}", "{stock_details.type}");'
    cursor.execute(sql)

# Fetch the stock details from the Polygon API.
for ticker in tickers:
    ticker_details = client.get_ticker_details(ticker)
    insert_stocks_into_table(ticker_details)

# Create the stock values tables
sql = """CREATE TABLE if not exists stock_values (
    stock_value_id INTEGER PRIMARY KEY,
    ticker TEXT not null,
    timestamp date,
    open real,
    high real,
    low real,
    close real,
    volume real,
    stock INTEGER not null,
    FOREIGN KEY (stock) REFERENCES stockss (stock_id)
    );"""
cursor.execute(sql)
con.commit()

# Insert all the stock values into the database
end = datetime.date.today() # The last day to get stock info for, using today.
period = datetime.timedelta(365+366) # The free API limits to the past 2 years of data so, 2 years with the possibility of there being a leap year.
start = end - period

def insert_values_into_table(stock, stock_values):
    """Inserts the stocks into the table. stock_values is a list of is a list of objects of type polygon.rest.models.Agg."""
    cursor.execute(f"select stock_id from stocks where ticker = '{stock}';")
    stock_id = cursor.fetchone()[0]
    for stock_value in stock_values:
        sql = """INSERT INTO stock_values 
            ('ticker', 'open', 'close', 'high', 'low', 'volume', 'timestamp', stock) 
            VALUES ("""
        sql += f"'{stock}', {stock_value.open}, {stock_value.close}, {stock_value.high}, {stock_value.low}, {stock_value.volume}, {stock_value.timestamp/1000}, {stock_id});"
        cursor.execute(sql)

for ticker in tickers:
    ticker_values = client.get_aggs(ticker, 1, "day", start, end) # get the ticker every 1 day between start and end
    insert_values_into_table(ticker, ticker_values)

con.commit()

con.close()
