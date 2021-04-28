import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def lookup(symbol):
    """Look up quote for symbol."""

    # Retrieve API key
    api_key = os.environ.get("IEX_API_KEY")

    # Contact API
    try:
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
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