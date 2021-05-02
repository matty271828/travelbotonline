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

# Thanks to CS50
def lookup(symbol):
    """Look up quote for symbol."""
    # Contact API
    try:
        url = f"{base_url}/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        print(f'API connection error: {response.status_code}')
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        print('Error')
        return None

def retrieve_symbols():
    """Retrieve all symbols supported by IEX Cloud for intra-day updates"""
    # Contact API
    try:
        url = f"{base_url}/ref-data/symbols?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        print(f'API connection error: {response.status_code}')
        return None

    # Parse response
    try:
        symbols = response.json()
        print("test")
        return None

    except (KeyError, TypeError, ValueError):
        print('Error')
        return None