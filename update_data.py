#%%
import asyncio
import builtins
from datetime import datetime
from pathlib import Path
import re
import sys

from api import tiingo
from db import db

rate_error_pattern = re.compile(r"^Error(.*)request allocation(.*)$")
def now():
    fmt = "%Y-%m-%d %H:%M:%S"
    return(datetime.now().strftime(fmt))
def print(*args, **kwargs):
    builtins.print(now(), *args, **kwargs)

async def update_meta(ticker):
    updated = False
    rate_limit_wait = 3600
    
    while not updated:
        try:
            print(f"({ticker}) - accessing meta data from tiingo", flush=True)
            meta_data = tiingo.get_meta(ticker)

            print(f"({ticker}) - writing meta data to database", flush=True)
            db.write_meta(meta_data["ticker"], meta_data["name"], meta_data["startDate"])
            updated = True
        except tiingo.RateLimitError:
            print(f"reached rate limit, retrying in {rate_limit_wait} seconds", flush=True)
            await asyncio.sleep(rate_limit_wait)

async def update_price(ticker):
    updated = False
    rate_limit_wait = 3600

    while not updated:
        try:
            print(f"({ticker}) - accessing price data from tiingo", flush=True)
            price_data = tiingo.get_price(ticker)

            print(f"({ticker}) - writing price data to database", flush=True)
            db.write_latest_price(ticker,
                price_data["open"],
                price_data["high"],
                price_data["low"],
                price_data["close"],
                price_data["volume"],
                price_data["date"])
            updated = True
        except tiingo.RateLimitError:
            print(f"reached rate limit, retrying in {rate_limit_wait} seconds", flush=True)
            await asyncio.sleep(10)

async def main():
    with open(Path(__file__).parent.joinpath("data/s&p500.csv"), "r") as readfile:
        ticker_pattern = re.compile(r"^[A-Z]+$")


        # generate coroutines
        coroutines = []
        for line in readfile:
            ticker = line.split(",")[0]
            print(ticker)
            if ticker_pattern.match(ticker):
                coroutines.append(update_meta(ticker))
                coroutines.append(update_price(ticker))

        # run coroutines
        await asyncio.gather(*coroutines)

        print("done")

if __name__ == "__main__":
    asyncio.run(main())