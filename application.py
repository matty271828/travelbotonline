"""
travelbotonline. Created by Matthew Maclean, 2021. 

The basic structure of this program expands upon the example provided by CS50x Problem Set 9 Finance. 
Many of the functions expand upon the examples provided. Throughout this program, where functions are 
taken directly, credit is given. 
"""
import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import psycopg2
import psycopg2.extras as ext
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import time

from run_sql import run_sql
from helpers import apology, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
	"""Renders index page"""
	return render_template("index.html")

@app.route("/browse", methods=["GET"])
def browse():
	"""Render browse page"""
	# Retrieve list of tickers

	# List of stocks to be displayed, each element is an array containing stock info
	stocks_list = ['test','test','test']

	return render_template("browse.html", stocks_list=stocks_list)

if __name__ == "__main__":
    app.run()