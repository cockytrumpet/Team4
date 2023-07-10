import os
import psycopg2
import flask
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.middleware.proxy_fix import ProxyFix
from markupsafe import escape
from helper import *
init_db()

app = Flask(__name__)
# not really 'secret', using os.environment for this one breaks production
app.config["SECRET_KEY"] = "df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506"
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

conn = get_db_connection()

# routes


@app.route("/")
def index():
    return render_template("index.html", page="home")


@app.route("/resources")
def resources():
    if not table_exists(conn, "resources"):
        return render_template(
            "notable.html", error="Resources", page="resources"
        )
    cur = conn.cursor()
    cur.execute(
        "SELECT resources.id, create_date, resources.title, resources.link, resources.descr, array_agg(tags.title) as tags "
        "FROM resources "
        "LEFT JOIN resource_tags ON resources.id = resource_tags.resource_id "
        "LEFT JOIN tags ON resource_tags.tag_id = tags.id "
        "GROUP BY resources.id "
        "ORDER BY create_date DESC;"
    )
    resources = cur.fetchall()
    cur.close()
    return render_template(
        "resources.html", resources=resources, page="resources"
    )


@app.route("/resourceform", methods=("GET", "POST"))
def resourceform():
    conn = get_db_connection()
    if request.method == "POST":
        title = escape(request.form["title"])
        link = escape(request.form["link"])
        descr = escape(request.form["descr"])
        tags = request.form.getlist("tags")
        resource_id = add_to_resources(title, link, descr, conn)

        for tag_id in tags:
            add_tag_to_resource(resource_id, int(tag_id), conn)

        return redirect(url_for("resources"))

    cur = conn.cursor()
    cur.execute("SELECT * FROM tags ORDER BY title ASC")
    tags = cur.fetchall()
    cur.close()
    return render_template("resource_form.html", tags=tags, page="resourceform")


@app.route("/projects")
def projects():
    if not table_exists(conn, "projects"):
        return render_template(
            "notable.html", error="Projects", page="projects"
        )
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT 0 as id, title, descr FROM projects ORDER BY title ASC;"
    )
    projects = cur.fetchall()
    cur.close()
    return render_template("projects.html", projects=projects, page="projects")


@app.route("/projectform", methods=("GET", "POST"))
def projectform():
    if request.method == "POST":
        title = escape(request.form["title"])
        descr = escape(request.form["descr"])
        add_to_projects(title, descr, conn)
        return redirect(url_for("projects"))
    return render_template("project_form.html", page="projectform")


@app.route("/tags")
def tags():
    if not table_exists(conn, "tags"):
        return render_template("notable.html", error="Tags", page="tags")
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT 0 as id, title, descr FROM tags ORDER BY title ASC;"
    )
    tags = cur.fetchall()
    cur.close()
    return render_template("tags.html", tags=tags, page="tags")


@app.route("/tagform", methods=("GET", "POST"))
def tagform():
    if request.method == "POST":
        title = escape(request.form["title"])
        descr = escape(request.form["descr"])
        add_to_tags(title, descr, conn)
        return redirect(url_for("tags"))
    return render_template("tag_form.html", page="tagform")


@app.errorhandler(404)
def page_not_found(error): 
    return render_template('404.html'), 404

def request_has_connection():
    return hasattr(flask.g, "dbconn")


def get_request_connection():
    if not request_has_connection():
        flask.g.dbconn = get_db_connection()
    return flask.g.dbconn


@app.teardown_request
def close_db_connection(ex):
    if request_has_connection():
        conn = get_request_connection()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)
