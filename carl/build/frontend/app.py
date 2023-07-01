import os
import psycopg2
from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    return conn


def make_db():
    conn = get_db_connection()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute("DROP TABLE IF EXISTS books;")
    cur.execute(
        "CREATE TABLE books (id serial PRIMARY KEY,"
        "title varchar (150) NOT NULL,"
        "author varchar (50) NOT NULL,"
        "pages_num integer NOT NULL,"
        "review text,"
        "date_added date DEFAULT CURRENT_TIMESTAMP);"
    )

    # Insert data into the table

    cur.execute(
        "INSERT INTO books (title, author, pages_num, review)"
        "VALUES (%s, %s, %s, %s)",
        ("A Tale of Two Cities", "Charles Dickens", 489, "A great classic!"),
    )

    cur.execute(
        "INSERT INTO books (title, author, pages_num, review)"
        "VALUES (%s, %s, %s, %s)",
        ("Anna Karenina", "Leo Tolstoy", 864, "Another great classic!"),
    )

    conn.commit()

    cur.close()
    conn.close()


@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books;")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", books=books)


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/tags")
def tags():
    return render_template("tags.html")


make_db()
if __name__ == "__main__":
    app.run(debug=True)
