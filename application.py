import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import psycopg2
import psycopg2.extras as ext
from run_sql import run_sql

from helpers import apology

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
app.config["SESSION_FILE_DIR"] = mkdtemp()
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
	# User reached  via post
	if request.method == 'POST':
		# Ensure username was submitted
		if not request.form.get("username"):
			return apology("Must provide username", 400)

		# Ensure password was submitted
		elif not request.form.get("password"):
			return apology("Must provide password", 400)

	else:	
		return render_template("login.html")

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
			return render_template("register.html")

	# User reached via get
	else:
		return render_template("register.html")

if __name__ == "__main__":
    app.run()

# SQL example code commented out for later use
# sql = "SELECT * FROM test_table"
# results = run_sql(sql)
# print(results)