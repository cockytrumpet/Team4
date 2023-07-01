import os
import psycopg2
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
#app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    return conn


def init():
    conn = get_db_connection()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    #############
    # Tag Table #
    #############
    cur.execute(
        "CREATE TABLE IF NOT EXISTS tags (id serial PRIMARY KEY,"
        "title varchar (150) NOT NULL,"
        "descr text);"
    )
    cur.execute(
        "INSERT INTO tags (title, descr)"
        "VALUES (%s, %s)",
        ("tag1", "descr"),
    )
    ###################
    # Resources Table #
    ###################
    cur.execute(
        "CREATE TABLE IF NOT EXISTS resources (id serial PRIMARY KEY,"
        "create_date DATE DEFAULT (CURRENT_DATE),"
        "title varchar (150) NOT NULL,"
        "link text,"
        "descr text);"
    )
    cur.execute(
        "INSERT INTO resources (title, link, descr)"
        "VALUES (%s, %s, %s)",
        ("Stack Overflow Article", "https://stackoverflow.com/questions/20461030/current-date-curdate-not-working-as-default-date-value","Current Date Function"),
    )
    #######################
    # ResourcesTags Table #
    #######################
    #cur.execute(
    #    "CREATE TABLE IF NOT EXISTS resourcestags (entry_id SERIAL PRIMARY KEY,"
    #    "FOREIGN KEY(resource_id) REFERENCES resources(id),"
    #    "FOREIGN KEY(tag_id) REFERENCES tags(id));"
    #)
    #cur.execute(
    #    "INSERT INTO resourcetags (title, link, descr)"
    #    "VALUES (%s, %s, %s)",
    #    ("Stack Overflow Article", "https://stackoverflow.com/questions/20461030/current-date-curdate-not-working-as-default-date-value","Current Date Function"),
    #)
    conn.commit()
    cur.close()
    conn.close()

def add_to_table(title,link,descr):
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()
    cur.execute(
    "CREATE TABLE IF NOT EXISTS resources (id serial PRIMARY KEY,"
    "create_date DATE DEFAULT (CURRENT_DATE),"
    "title varchar (150) NOT NULL,"
    "link text,"
    "descr text);"
    )
    cur.execute(
    "INSERT INTO resources (title, link, descr)"
    "VALUES (%s, %s, %s)",
    (title, link, descr),
    )
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM resources;")
    tags = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", books=tags)


@app.route("/home")
def home():
    return "<p>Home!</p>"

@app.route("/create", methods=('GET','POST'))
def create():
    if request.method == 'POST':
        title = str(request.form['title'])
        link = str(request.form['link'])
        descr = str(request.form['descr'])
        add_to_table(title,link,descr)

        return redirect(url_for('index'))
    return render_template('form.html')

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/tags")
def tags():
    return render_template("tags.html")

if __name__ == "__main__":
    app.run(debug=True)