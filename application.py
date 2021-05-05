"""
ValueMe. Created by Matthew Maclean, 2021. 

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
from contact_api import lookup, retrieve_symbols

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

@app.route("/login", methods=["GET", "POST"])
def login():
	"""Log user in"""
	# Forget any user_id
	session.clear()

	# User reached  via post
	if request.method == 'POST':
		# Ensure username was submitted
		if not request.form.get("username"):
			return apology("Must provide username", 403)

		# Ensure password was submitted
		elif not request.form.get("password"):
			return apology("Must provide password", 403)

		# Query database for username
		sql = "SELECT * FROM users WHERE username = (%s)"
		values = [request.form.get("username")]
		rows = run_sql(sql, values)

		#print(rows)

		# Ensure username exists 
		if len(rows) != 1:
			return apology("User does not exist", 403)
		
		# Ensure password is correct
		if not check_password_hash(rows[0]["hash"], request.form.get("password")):
			return apology("invalid password", 403)

		# Remember which user has logged in
		#print(rows[0]["id"])
		session["user_id"] = rows[0]["id"]

		# Redirect user to browse page
		return redirect("/browse")

	else:	
		return render_template("login.html")

# Thanks to CS50
@app.route("/logout")
def logout():
	"""Log user out"""

	# Forget any user_id
	session.clear()

	# Redirect user to home page
	return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
	"""Register user account"""
	# User reached via post
	if request.method == 'POST':

		# Ensure username was submitted
		if not request.form.get("username"):
			return apology("Must provide username", 400)

		# Ensure password was submitted
		elif not request.form.get("password"):
			return apology("Must provide password", 400)

		# Ensure confirm password was submitted
		elif not request.form.get("confirmation"):
			return apology("Must confirm password", 400)

		# Ensure confirm password matches password
		elif request.form.get("password") != request.form.get("confirmation"):
			return apology("Password does not match password confirmation", 400)

		else:
			# Check for username already existing in database
			sql = "SELECT DISTINCT username FROM users"
			users = run_sql(sql)

			for user in users:
				if user['username'] == request.form.get("username"):
					return apology("Username not available!", 400)
				else:
					pass

			# Hash the users password
			password_hash = generate_password_hash(request.form.get("password"))

			# Find max previously used id number and assign new number
			sql = "SELECT id FROM users ORDER BY id DESC LIMIT 1"
			prev_ids = run_sql(sql)
			if prev_ids == []:
				new_id = 1
			else:
				new_id = int(prev_ids[0][0]) + 1

			# Insert new user into database
			sql = "INSERT INTO users (id, username, hash) VALUES (%s,%s,%s)"
			values = [new_id, request.form.get("username"), password_hash]
			results = run_sql(sql, values)

			# redirect 
			return redirect("/login")

	# User reached via get
	else:
		return render_template("register.html")

@app.route("/browse", methods=["GET"])
def browse():
	"""Render browse page"""
	# Retrieve list of tickers
	sql = "SELECT ticker FROM watchlist_requests WHERE user_id = (%s)"
	values = [session["user_id"]]
	tickers = run_sql(sql, values)

	print(tickers)
	for ticker in tickers:
		print(ticker[0])

	# List of stocks to be displayed, each element is an array containing stock info
	stocks_list = []

	# Contact API
	for ticker in tickers:
		stock_info = lookup(ticker[0])
		stocks_list.append(stock_info)

	return render_template("browse.html", stocks_list=stocks_list)

@app.route("/watchlist", methods=["GET", "POST"])
def watchlist():
	"""Render browse page"""
	# User reached via POST
	if request.method == "POST":
		# Ticker 
		ticker = request.form.get("symbol")

		# Insert into database
		sql = "INSERT INTO watchlist_requests (ticker, user_id) VALUES (%s, %s)"
		values = [ticker, session["user_id"]]
		results = run_sql(sql, values)

		# Return to watchlist page
		return render_template("watchlist.html")

	# Else
	else:
		# Query API for all stocks
		tickers = retrieve_symbols()

		# Render template
		return	render_template("watchlist.html", tickers=tickers)

if __name__ == "__main__":
    app.run()