import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

# Manually change API_environment variable here to access either production or sandbox API
# Configure API to access real data 
API_environment = 'sandbox'
if API_environment == 'prod':
    base_url = "https://cloud.iexapis.com/stable"
    api_key = os.environ.get("IEX_API_KEY")
# Configure for sandbox data
else:
    base_url = "https://sandbox.iexapis.com/stable"
    api_key = os.environ.get("IEX_TEST_KEY")
    os.environ['IEX_SANDBOX'] = 'enable'

# Thanks to CS50 for core code of this function
def make_request(get_parameter):
    """Contact API, input IEX get request parameter and output json data"""
    # Contact API
    try:
        url = f"{base_url}{get_parameter}?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        print(f'API connection error: {response.status_code}')
        return None

    # Parse response
    try:
        return response.json()
    
    except (KeyError, TypeError, ValueError):
        print('Key, Type or Value Error has occurred')
        return None

# Lookup quotation for symbol
def lookup(symbol):
    """Look up quote for symbol."""
    # Format get_parameter
    get_parameter = f"/stock/{urllib.parse.quote_plus(symbol)}/quote"

    # Contact API
    quote = make_request(get_parameter)

    # Return data
    try:
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    
    except (KeyError, TypeError, ValueError):
        print("Error")
        return None

def retrieve_symbols():
    """Retrieve all symbols supported by IEX Cloud for intra-day updates"""
    # Format get_parameter
    get_parameter = f"/ref-data/symbols"

    # Contact API
    symbols_dict = make_request(get_parameter)

    # Collect tickers only (other data is included in json response)
    # Refer to IEX documentation for json output format
    tickers = []
    for symbol in symbols_dict:
        tickers.append(symbol["symbol"])
        
    # Return data
    return tickers
