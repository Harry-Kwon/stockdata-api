#%%
from pathlib import Path
import re
import sys

if len(sys.argv)<2:
  print("usage: update_data [ticker]")
  exit(-1)

from api import tiingo
from db import db

ticker = sys.argv[1]

def update_meta(ticker):
    meta_data = tiingo.get_meta(ticker)
    db.write_meta(meta_data["ticker"], meta_data["name"], meta_data["startDate"])

def update_price(ticker):
    price_data = tiingo.get_price(ticker)
    db.write_latest_price(ticker,
        price_data["open"],
        price_data["high"],
        price_data["low"],
        price_data["close"],
        price_data["volume"])


with open(Path(__file__).parent.joinpath("data/s&p500.csv"), "r") as readfile:
    ticker_pattern = re.compile(r"^[A-Z]*$")
    for line in readfile:
        ticker = line.split(",")[0]
        if ticker_pattern.match(ticker):
            update_meta(ticker)