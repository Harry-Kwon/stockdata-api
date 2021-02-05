#%%
import json
from pathlib import Path
import re
import requests

class Error(Exception):
    """Base Exception class"""
    pass

class RateLimitError(Error):
    """Exception raised for rate limit exceeded errors

    Attributes:
        query -- query for which the error occured
        message -- error message from the tiingo api
    """
    def __init__(self, query, message):
        self.message = message

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

rate_error_pattern = re.compile(r"^Error(.*)request allocation(.*)$")

def get_meta(ticker):
    uri = meta_endpoint.replace("<ticker>", ticker)
    response = requests.get(uri, headers=standard_headers).json()
    if ("detail" in response) and (rate_error_pattern.match(response["detail"])):
        raise RateLimitError(uri, response["detail"])
    else:
        return(response)

def get_price(ticker):
    uri = price_endpoint.replace("<ticker>", ticker)
    response = requests.get(uri, headers=standard_headers).json()

    if ("detail" in response) and (rate_error_pattern.match(response["detail"])):
        raise RateLimitError(uri, response["detail"])
    else:
        return(response[0])

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