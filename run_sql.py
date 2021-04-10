import psycopg2
import psycopg2.extras as ext
import os

# Set environment variable
ENV = 'dev'
# Run local database
if ENV == 'dev':
    DATABASE_URL = os.environ.get('local_database_url')
# Run production database
else:
    DATABASE_URL = os.environ.get('production_database_url')

# Function to run SQL queries 
def run_sql(sql, values = None):
    conn = None
    results = []

    try:
        # conn=psycopg2.connect("dbname='lingua_snaps'")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=ext.DictCursor)
        cur.execute(sql, values)
        conn.commit()
        results = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return results