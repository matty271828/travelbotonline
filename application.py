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
from helpers import apology, gbp

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
app.jinja_env.filters["gbp"] = gbp

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
	# Retrieve list of flights to be displayed
	sql = "SELECT * FROM best_flights"
	flights = run_sql(sql)
	
	# List of flights to be displayed, each element is an array containing stock info
	flights_list = []

	# Add results into flights_list
	for flight in flights:
		flight_dict = {}

		flight_dict['source'] = flight[1]
		flight_dict['dest'] = flight[2]
		flight_dict['price'] = flight[3]
		flight_dict['outdate'] = flight[4]
		flight_dict['indate'] = flight[5]
		flight_dict['origin_id'] = flight[6]
		flight_dict['dest_id'] = flight[7]

		flights_list.append(flight_dict)

	print(flights_list)

	return render_template("browse.html", flights_list=flights_list)

if __name__ == "__main__":
    app.run()