import os
import psycopg2
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


def table_exists(con, table_str):
    exists = False
    try:
        cur = con.cursor()
        cur.execute(
            "select exists(select relname from pg_class where relname='"
            + table_str
            + "')"
        )
        exists = cur.fetchone()[0]
        print(exists)
        cur.close()
    except psycopg2.Error as e:
        print(e)
    return exists


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
        "INSERT INTO tags (title, descr)" "VALUES (%s, %s)",
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
        "INSERT INTO resources (title, link, descr)" "VALUES (%s, %s, %s)",
        (
            "Stack Overflow Article",
            "https://stackoverflow.com/questions/20461030/current-date-curdate-not-working-as-default-date-value",
            "Current Date Function",
        ),
    )
    #######################
    # ResourcesTags Table #
    #######################
    # cur.execute(
    #    "CREATE TABLE IF NOT EXISTS resourcestags (entry_id SERIAL PRIMARY KEY,"
    #    "FOREIGN KEY(resource_id) REFERENCES resources(id),"
    #    "FOREIGN KEY(tag_id) REFERENCES tags(id));"
    # )
    # cur.execute(
    #    "INSERT INTO resourcetags (title, link, descr)"
    #    "VALUES (%s, %s, %s)",
    #    ("Stack Overflow Article", "https://stackoverflow.com/questions/20461030/current-date-curdate-not-working-as-default-date-value","Current Date Function"),
    # )
    conn.commit()
    cur.close()
    conn.close()


def add_to_table(title, link, descr):
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
        "INSERT INTO resources (title, link, descr)" "VALUES (%s, %s, %s)",
        (title, link, descr),
    )
    conn.commit()
    cur.close()
    conn.close()


def add_to_tags(title, descr):
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS tags (id serial PRIMARY KEY,"
        "title varchar (150) NOT NULL,"
        "descr text);"
    )
    cur.execute(
        "INSERT INTO tags (title, descr)" "VALUES (%s, %s)",
        (title, descr),
    )
    conn.commit()
    cur.close()
    conn.close()

def add_to_projects(title, descr):
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS projects (id serial PRIMARY KEY,"
        "title varchar (150) NOT NULL,"
        "descr text);"
    )
    cur.execute(
        "INSERT INTO projects (title, descr)" "VALUES (%s, %s)",
        (title, descr),
    )
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/resources")
def resources():
    conn = get_db_connection()
    if not table_exists(conn, "resources"):
        return render_template("notable.html", error="Resources")
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT 0 AS id, create_date, title, link, descr FROM resources ORDER BY create_date DESC;"
    )
    tags = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("resources.html", books=tags)

@app.route("/resourceform", methods=("GET", "POST"))
def resourceform():
    if request.method == "POST":
        title = str(request.form["title"])
        link = str(request.form["link"])
        descr = str(request.form["descr"])
        add_to_table(title, link, descr)
        return redirect(url_for("resources"))
    return render_template("resource_form.html")


@app.route("/projects")
def projects():
    conn = get_db_connection()
    if not table_exists(conn, "projects"):
        return render_template("notable.html", error="Projects")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT 0 as id, title, descr FROM projects ORDER BY title ASC;")
    tags = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("projects.html", books=tags)

@app.route("/projectform", methods=("GET", "POST"))
def projectform():
    if request.method == "POST":
        title = str(request.form["title"])
        descr = str(request.form["descr"])
        add_to_projects(title, descr)
        return redirect(url_for("projects"))
    return render_template("project_form.html")

@app.route("/tags")
def tags():
    conn = get_db_connection()
    if not table_exists(conn, "tags"):
        return render_template("notable.html", error="Tags")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT 0 as id, title, descr FROM tags ORDER BY title ASC;")
    tags = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("tags.html", books=tags)


@app.route("/tagform", methods=("GET", "POST"))
def tagform():
    if request.method == "POST":
        title = str(request.form["title"])
        descr = str(request.form["descr"])
        add_to_tags(title, descr)
        return redirect(url_for("tags"))
    return render_template("tag_form.html")


if __name__ == "__main__":
    app.run(debug=True)
