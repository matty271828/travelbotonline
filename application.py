import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
import psycopg2

# Configure application
app = Flask(__name__)

# Set environment variable
ENV = 'dev'

# Run local database
if ENV == 'dev':
	app.debug == True
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('local_database_url')

# Run production database
else:
	app.debug == False
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('production_database_url')

# Set track modifications to false
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Create database object
db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)

    def __init__(self, amount):
    	self.amount = amount

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
	return render_template("index.html", test_value)

@app.route("/login")
def login():
	"""Log user in"""
	test_value = db.column(1)

	return render_template("login.html", test_value)

if __name__ == "__main__":
    app.run()