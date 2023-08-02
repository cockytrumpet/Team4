import flask
from flask import Flask, render_template, url_for, flash, redirect, request
from werkzeug.middleware.proxy_fix import ProxyFix
from markupsafe import escape
from helper import *

# We don't need to initialize the database every time we run the application
# Our database information is persistent storage, and stored for use between instances of the application
# The only thing we need to do every time is establish a connection to the database
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


@app.route("/resources", defaults={"tag": "ALL"})
@app.route("/resources/<tag>")
def resources(tag="ALL", message=None):
    if not table_exists(conn, "resources"):
        return render_template(
            "notable.html", error="Resources", page="resources"
        )
    if tag == "ALL":
        return render_template(
            "resources.html",
            resources=get_resources(conn),
            tags=get_tags(conn),
            page="resources",
            message=message,
        )
    else:
        return render_template(
            "resources.html",
            resources=get_tagged_resources(tag, conn),
            tags=get_tags(conn),
            page="resources",
            message=message,
        )


@app.route("/resourceform", methods=("GET", "POST"))
def resourceform():
    message = None
    if request.method == "POST":
        title = escape(request.form["title"])
        link = escape(request.form["link"])
        descr = escape(request.form["descr"])
        tags = request.form.getlist("tags")
        message = add_to_resources(title, link, descr, conn)

        if message[0] == "success":
            resource_id = get_rescource_id_by_title(title, conn)
            for tag_id in tags:
                add_tag_to_resource(resource_id, int(tag_id), conn)
            return resources(message=message)

    return render_template(
        "resource_form.html",
        tags=get_tags(conn),
        page="resources",
        message=message,
    )


@app.route("/resource/<int:id>/delete", methods=("POST",))
def delete_resource(id):
    get_resource = get_resource_by_id(id, conn)
    if get_resource is None:
        message = ("error", "Resource not found")
    else:
        delete_resource_by_id(id, conn)
        message = ("success", "Resource deleted")
    return resources(message=message)


@app.route("/edit_resource/<int:id>", methods=("GET", "POST"))
def edit_resource(id):
    message = None
    if request.method == "POST":
        title = escape(request.form["title"])
        link = escape(request.form["link"])
        descr = escape(request.form["descr"])
        tags = request.form.getlist("tags")

        message = update_resource(id, title, link, descr, tags, conn)
        if message[0] == "success":
            return resources(message=message)

    resource = get_resource(id, conn)
    # print("Resource Tags: ", resource[5])  # Debug statement
    all_tags = get_tags(conn)
    # print("All Tags: ", all_tags)  # Debug statement
    return render_template(
        "edit_resource.html",
        resource=resource,
        tags=all_tags,
        page="resources",
        message=message,
    )


@app.route("/projects")
def projects(message=None):
    if not table_exists(conn, "projects"):
        return render_template(
            "notable.html", error="Projects", page="projects"
        )
    return render_template(
        "projects.html",
        projects=get_projects(conn),
        page="projects",
        message=message,
    )


@app.route("/projectform", methods=("GET", "POST"))
def projectform():
    message = None
    if request.method == "POST":
        title = escape(request.form["title"])
        descr = escape(request.form["descr"])
        message = add_to_projects(title, descr, conn)
        if message[0] == "success":
            return projects(message=message)
    return render_template(
        "project_form.html", page="projectform", message=message
    )


@app.route("/project/<int:id>/delete", methods=("POST",))
def delete_project(id):
    project = get_project_by_id(id, conn)
    if project is None:
        message = ("error", "Project not found")
    else:
        delete_project_by_id(id, conn)
        message = ("success", "Project deleted")
    return projects(message=message)


# @app.route("/edit_project/<int:id>", methods=("GET", "POST"))
# def edit_project(id):
#     if request.method == "POST":
#         title = escape(request.form["title"])
#         descr = escape(request.form["descr"])

#         update_project(id, title, descr, conn)

#         return redirect(url_for("projects"))
#     else:
#         tag = get_project_by_id(id, conn)
#         return render_template(
#             "edit_project.html",
#             project=project,
#             page="projects",
#         )


@app.route("/tags")
def tags(message=None):
    if not table_exists(conn, "tags"):
        return render_template("notable.html", error="Tags", page="tags")
    return render_template(
        "tags.html", tags=get_tags(conn), page="tags", message=message
    )


@app.route("/tagform", methods=("GET", "POST"))
def tagform():
    message = None
    if request.method == "POST":
        title = escape(request.form["title"])
        descr = escape(request.form["descr"])
        message = add_to_tags(title, descr, conn)
        if message[0] == "success":
            return tags(message)
    return render_template("tag_form.html", page="tags", message=message)


@app.route("/tag/<int:id>/delete", methods=("POST",))
def delete_tag(id):
    tag = get_tag_by_id(id, conn)
    if tag is None:
        message = ("error", "Tag not found")
    else:
        delete_tag_by_id(id, conn)
        message = ("success", "Tag deleted")
    return tags(message)


@app.route("/edit_tag/<int:id>", methods=("GET", "POST"))
def edit_tag(id):
    message = None
    if request.method == "POST":
        title = escape(request.form["title"])
        descr = escape(request.form["descr"])

        message = update_tag(id, title, descr, conn)
        if message[0] == "success":
            return tags(message)

    tag = get_tag_by_id(id, conn)
    return render_template(
        "edit_tag.html", tag=tag, page="tags", message=message
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route("/find", methods=("GET", "POST"))
def find():
    if request.method == "POST":
        tags = escape(request.form["tags"])
        return render_template(
            "resources.html",
            resources=search_resources(tags, conn),
            tags=get_tags(conn),
            page="resources",
        )
    return render_template("find.html", page="resources")


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
