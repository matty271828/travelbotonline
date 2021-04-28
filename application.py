import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import psycopg2
import psycopg2.extras as ext
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from run_sql import run_sql
from helpers import apology
from contact_api import lookup

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

		# Redirect user to home page
		return redirect("/")

	else:	
		return render_template("login.html")

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
	# List of tickers
	tickers = ["TSLA","AAPL","WKHS","FB","ACTC","MSFT","GOOG","PFE","NKE"]

	# List of stocks to be displayed, each element is an array containing stock info
	stocks_list = []

	# Populate a dictionary with ticker, name and current price for ticker
	for ticker in tickers:
		# Lookup ticker
		stock_info = lookup(ticker)

		# Add to dictionary
		stocks_list.append(stock_info)

	print(stocks_list)	

	return render_template("browse.html", stocks_list=stocks_list)

if __name__ == "__main__":
    app.run()