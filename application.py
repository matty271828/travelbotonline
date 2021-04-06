from flask import Flask, render_template
import os
import psycopg2

# Configure application
app = Flask(__name__)

# Connect to database
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()

# Test comment 1
