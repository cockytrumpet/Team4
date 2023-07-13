import os
import psycopg2
import flask
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.middleware.proxy_fix import ProxyFix
from markupsafe import escape
import helper as h

app = Flask(__name__)
# not really 'secret', using os.environment for this one breaks production
app.config["SECRET_KEY"] = "df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506"
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

conn = h.get_db_connection()

# routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/resources")
def resources():
    if not h.table_exists(conn, "resources"):
        return render_template("notable.html", error="Resources")
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT 0 AS id, create_date, title, link, descr FROM resources ORDER BY create_date DESC;"
    )
    resources = cur.fetchall()
    cur.close()
    #conn.close()
    return render_template("resources.html", resources=resources)


@app.route("/resourceform", methods=("GET", "POST"))
def resourceform():
    if request.method == "POST":
        title = escape(request.form["title"])
        link = escape(request.form["link"])
        descr = escape(request.form["descr"])
        tag = escape(request.form.get("tag"))
        tag = tag[6:-7]
        h.add_to_resources(title, link, descr, conn, tag)

        return redirect(url_for("resources"))

    cur = conn.cursor()
    cur.execute(
            "SELECT DISTINCT title FROM tags GROUP BY id;"
    )
    tags = cur.fetchall()
    cur.close()
    return render_template("resource_form.html", tags=tags)


@app.route("/projects")
def projects():
    #conn = h.get_db_connection()
    if not h.table_exists(conn, "projects"):
        return render_template("notable.html", error="Projects")
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT 0 as id, title, descr FROM projects ORDER BY title ASC;"
    )
    projects = cur.fetchall()
    cur.close()
    #conn.close()
    return render_template("projects.html", projects=projects)


@app.route("/projectform", methods=("GET", "POST"))
def projectform():
    if request.method == "POST":
        title = escape(request.form["title"])
        descr = escape(request.form["descr"])
        h.add_to_projects(title, descr,conn)
        return redirect(url_for("projects"))
    return render_template("project_form.html")


@app.route("/tags")
def tags():
    #conn = h.get_db_connection()
    if not h.table_exists(conn, "tags"):
        return render_template("notable.html", error="Tags")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT 0 as id, title, descr FROM tags ORDER BY title ASC;")
    tags = cur.fetchall()
    cur.close()
    #conn.close()
    return render_template("tags.html", tags=tags)


@app.route("/tagform", methods=("GET", "POST"))
def tagform():
    if request.method == "POST":
        title = escape(request.form["title"])
        descr = escape(request.form["descr"])
        h.add_to_tags(title, descr,conn)
        return redirect(url_for("tags"))
    return render_template("tag_form.html")

@app.route("/find", methods=("GET", "POST"))
def find():
    if request.method == "POST":
        tag = escape(request.form["tag"])
        cur = conn.cursor()
        cur.execute(
            f"SELECT DISTINCT 0 as id, r.create_date, r.title, r.link, r.descr FROM resources AS r LEFT JOIN tags AS t ON t.id = r.id WHERE '{tag}' IN (SELECT DISTINCT title FROM tags)"
        )
        resources = cur.fetchall()
        cur.close()
        return render_template("resources.html", resources=resources)
    return render_template("find.html")


def request_has_connection():
    return hasattr(flask.g, 'dbconn')

def get_request_connection():
    if not request_has_connection():
        flask.g.dbconn = h.get_db_connection()
    return flask.g.dbconn

@app.teardown_request
def close_db_connection(ex):
    if request_has_connection():
        conn = get_request_connection()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)