#%%
import json
from pathlib import Path
import requests

# load api key from secrets file
with open(Path(__file__).parent.joinpath("../secrets.json"), "r") as readfile:
    data = json.load(readfile)
    api_token = data["api"]["api_token"]

# api endpoints
meta_endpoint = "https://api.tiingo.com/tiingo/daily/<ticker>"
price_endpoint = "https://api.tiingo.com/tiingo/daily/<ticker>/prices"
historic_endpoint = "https://api.tiingo.com/tiingo/daily/<ticker>/prices?startDate=<start_date>&endDate=<end_date>"
standard_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {api_token}"
}

def get_meta(ticker):
    uri = meta_endpoint.replace("<ticker>", ticker)
    response = requests.get(uri, headers=standard_headers)
    return(response.json())

def get_price(ticker):
    uri = price_endpoint.replace("<ticker>", ticker)
    response = requests.get(uri, headers=standard_headers)
    return(response.json()[0])

def get_historic(ticker, start_date, end_date):
    fmt = "%Y-%m-%d"

    uri = historic_endpoint.replace("<ticker>", ticker)
    uri = uri.replace("<start_date>", start_date.strftime(fmt))
    uri = uri.replace("<end_date>", end_date.strftime(fmt))

    response = requests.get(uri, headers=standard_headers)
    return(response.json())

def test_connection():
    response = requests.get("https://api.tiingo.com/api/test/",
        headers=standard_headers)
    return(response.json())

if __name__ == "__main__":
    print(test_connection())