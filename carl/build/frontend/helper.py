import os
import psycopg2


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create resources table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS resources (id serial PRIMARY KEY,"
        "create_date DATE DEFAULT (CURRENT_DATE),"
        "title varchar (150) NOT NULL,"
        "link text,"
        "descr text);"
    )

    # Create tags table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS tags (id serial PRIMARY KEY,"
        "title varchar (150) NOT NULL,"
        "descr text);"
    )

    # Create projects table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS projects (id serial PRIMARY KEY,"
        "title varchar (150) NOT NULL,"
        "descr text);"
    )

    # Create resource_tags table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS resource_tags (id serial PRIMARY KEY,"
        "resource_id integer,"
        "tag_id integer,"
        "FOREIGN KEY (resource_id) REFERENCES resources (id),"
        "FOREIGN KEY (tag_id) REFERENCES tags (id));"
    )

    # Create projects_resources table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS project_resources (id serial PRIMARY KEY,"
        "project_id integer,"
        "resource_id integer,"
        "FOREIGN KEY (project_id) REFERENCES projects (id),"
        "FOREIGN KEY (resource_id) REFERENCES resources (id));"
    )

    # Create projects_tags table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS project_tags (id serial PRIMARY KEY,"
        "project_id integer,"
        "tag_id integer,"
        "FOREIGN KEY (project_id) REFERENCES projects (id),"
        "FOREIGN KEY (tag_id) REFERENCES tags (id));"
    )

    conn.commit()
    cur.close()
    conn.close()


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
        # print(exists)
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


def add_to_resources(title, link, descr, conn):
    message = None

    # Check for empty fields
    if title == "":
        message = ("error", "Title cannot be empty")
        return message

    if link == "":
        message = ("error", "Link cannot be empty")
        return message

    if link[:5].lower() != "http":
        link = "http://" + link

    # Check if resource already exists
    cur = conn.cursor()
    cur.execute("SELECT * FROM resources WHERE title = %s", (title,))
    resource_exists = cur.fetchone()

    if resource_exists:
        cur.close()
        message = ("error", "Resource already exists")
        return message

    # Open a cursor to perform database operations
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

    message = ("success", f"Resource {title} added")
    return message


def get_rescource_id_by_title(title, conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM resources WHERE title = %s", (title,))
    resource_id = cur.fetchone()
    cur.close()
    return resource_id


def get_resource_by_id(id, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM resources WHERE id = %s", (id,))
    resource = cur.fetchone()
    cur.close()
    return resource


def delete_resource_by_id(id, conn):
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM resource_tags WHERE resource_id = %s",
        (id,),  # delete tag relations first
    )
    cur.execute(
        "DELETE FROM resources WHERE id = %s", (id,)  # then delete resource
    )
    conn.commit()
    cur.close()


def get_resource(id, conn):
    with conn.cursor() as cur:
        cur.execute(
            """
        SELECT resources.id, create_date, resources.title, resources.link, resources.descr, array_agg(tags.title) as tags, array_agg(projects.title) as projects
        FROM resources
        LEFT JOIN resource_tags ON resources.id = resource_tags.resource_id
        LEFT JOIN tags ON resource_tags.tag_id = tags.id
        LEFT JOIN project_resources ON resources.id = project_resources.resource_id
        LEFT JOIN projects ON project_resources.project_id = projects.id
        WHERE resources.id=%s
        GROUP BY resources.id
        """,
            (id,),
        )
        resource = cur.fetchone()
    return resource


def update_resource(id, title, link, descr, tags, conn):
    message = None

    # Check for empty fields
    if title == "":
        message = ("error", "Title cannot be empty")
        return message

    if link == "":
        message = ("error", "Link cannot be empty")
        return message

    if link[:5].lower() != "http":
        link = "http://" + link

    # If they change the title, check if the new title already exists.
    cur = conn.cursor()
    cur.execute("SELECT title FROM resources WHERE id = %s", (id,))
    current_title = cur.fetchone()[0]

    resource_exists = False
    if current_title != title:
        cur.execute(
            "SELECT COUNT(*) FROM resources WHERE title = %s", (title,)
        )
        resource_exists = cur.fetchone()[0]

    if resource_exists:
        cur.close()
        message = ("error", "Resource already exists")
        return message

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE resources SET title=%s, link=%s, descr=%s WHERE id=%s",
            (title, link, descr, id),
        )
        # Assuming you have a separate table for resource_tags relationship
        cur.execute("DELETE FROM resource_tags WHERE resource_id=%s", (id,))
        for tag in tags:
            cur.execute(
                "INSERT INTO resource_tags (resource_id, tag_id) VALUES (%s, %s)",
                (id, tag),
            )
    conn.commit()
    message = ("success", f"Resource {title.unescape()} updated")
    return message


def add_to_tags(title, descr, conn):
    message = None

    if title == "":
        message = ("error", "Title cannot be empty")
        return message

    # Create table if it does not exist.
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS tags (id serial PRIMARY KEY,"
        "title varchar (150) NOT NULL,"
        "descr text);"
    )

    # Check if tag exists.
    cur.execute("SELECT COUNT(*) FROM tags WHERE title = %s", (title,))
    tag_exists = cur.fetchone()[0]

    if tag_exists:
        # If the tag already exists, close the cursor and return False.
        cur.close()
        message = ("error", "Tag already exists")
        return message

    # If the tag does not exist, create it
    cur.execute(
        "INSERT INTO tags (title, descr) VALUES (%s, %s)",
        (title, descr),
    )
    conn.commit()
    cur.close()
    message = ("success", f"Tag {title} added")
    return message


def get_tag_by_id(id, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tags WHERE id = %s", (id,))
    tag = cur.fetchone()
    cur.close()
    return tag


def delete_tag_by_id(id, conn):
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM resource_tags WHERE tag_id = %s",
        (id,),  # delete tag relations first
    )
    cur.execute("DELETE FROM tags WHERE id = %s", (id,))  # then delete tag
    conn.commit()
    cur.close()


def update_tag(id, title, descr, conn):
    if title == "":
        message = ("error", "Title cannot be empty")
        return message

    # If they change the title, check if the new title already exists.
    cur = conn.cursor()
    cur.execute("SELECT title FROM tags WHERE id = %s", (id,))
    current_title = cur.fetchone()[0]

    tag_exists = False
    if current_title != title:
        cur.execute("SELECT COUNT(*) FROM tags WHERE title = %s", (title,))
        tag_exists = cur.fetchone()[0]

    if tag_exists:
        cur.close()
        message = ("error", "Tag already exists")
        return message

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE tags SET title=%s, descr=%s WHERE id=%s",
            (title, descr, id),
        )
    conn.commit()
    message = ("success", f"Tag {title.unescape()} updated")
    return message


def add_to_projects(title, descr, conn):
    message = None

    if title == "":
        message = ("error", "Title cannot be empty")
        return message

    # create table if it does not exist
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS projects (id serial PRIMARY KEY,"
        "title varchar (150) NOT NULL,"
        "descr text);"
    )

    # check if project exists
    cur.execute("SELECT COUNT(*) FROM projects WHERE title = %s", (title,))
    project_exists = cur.fetchone()[0]

    if project_exists:
        cur.close()
        message = ("error", "Project already exists")
        return message

    cur.execute(
        "INSERT INTO projects (title, descr)" "VALUES (%s, %s)",
        (title, descr),
    )
    conn.commit()
    cur.close()
    message = ("success", f"Project {title.unescape()} added")
    return message


def add_resource_to_project(conn, project_id, resource_id):
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO project_resources (project_id, resource_id)" "VALUES (%s, %s)",
        (project_id, resource_id),
    )
    conn.commit()


def get_tags(conn):
    cur = conn.cursor()
    # TODO: maybe we should be ensureing no duplicates on input instead of here
    # cur.execute("SELECT DISTINCT 0 as id, title, descr FROM tags ORDER BY title ASC;")
    cur.execute("SELECT * FROM tags ORDER BY title ASC")
    tags = cur.fetchall()
    cur.close()
    return tags


def get_projects(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects ORDER BY title ASC;")
    projects = cur.fetchall()
    cur.close()
    return projects


def get_project_by_id(id, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE id = %s", (id,))
    project = cur.fetchone()
    cur.close()
    return project


def delete_project_by_id(id, conn):
    cur = conn.cursor()
    ############  implement once resources can be assinged to projects #########
    # cur.execute(
    #     "DELETE FROM project_resources WHERE project_id = %s",
    #     (id,),  # delete tag relations first
    # )
    cur.execute("DELETE FROM projects WHERE id = %s", (id,))  # then delete tag
    conn.commit()
    cur.close()


def get_resources(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT resources.id, create_date, resources.title, resources.link, resources.descr, array_agg(tags.title) as tags, array_agg(projects.title) as projects "
        "FROM resources "
        "LEFT JOIN resource_tags ON resources.id = resource_tags.resource_id "
        "LEFT JOIN tags ON resource_tags.tag_id = tags.id "
        "LEFT JOIN project_resources ON resources.id = project_resources.resource_id "
        "LEFT JOIN projects ON project_resources.project_id = projects.id "
        "GROUP BY resources.id "
        "ORDER BY title ASC;"
    )
    resources = cur.fetchall()
    cur.close()
    return resources


def add_tag_to_resource(resource_id, tag_id, conn):
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS resource_tags (id serial PRIMARY KEY,"
        "resource_id integer,"
        "tag_id integer,"
        "FOREIGN KEY (resource_id) REFERENCES resources (id),"
        "FOREIGN KEY (tag_id) REFERENCES tags (id));"
    )
    cur.execute(
        "INSERT INTO resource_tags (resource_id, tag_id)" "VALUES (%s, %s)",
        (resource_id, tag_id),
    )
    conn.commit()
    cur.close()


def get_tagged_resources(tag_id, conn):
    curr = conn.cursor()
    # SQL query to select all rows from the resource table where the tag_id is in the resource_tags table
    # note from TE - technically joins are faster than nested queries (not super important but just for fun)
    curr.execute(
        "SELECT resources.id, create_date, resources.title, resources.link, resources.descr, array_agg(tags.title) as tags "
        "FROM resources "
        "LEFT JOIN resource_tags ON resources.id = resource_tags.resource_id "
        "LEFT JOIN tags ON resource_tags.tag_id = tags.id "
        f"WHERE tags.id = {tag_id} "
        "GROUP BY resources.id "
        "ORDER BY create_date DESC;"
        # f"""
        # SELECT
        # *
        # FROM resources AS r
        # LEFT JOIN resource_tags AS rt ON rt.resource_id = r.id
        # INNER JOIN tags AS t ON t.id = rt.tag_id
        # WHERE t.id = {tag_id}
        # ORDER BY r.id DESC
        # """
    )
    # SELECT * FROM resources AS r WHERE id IN (SELECT resource_id FROM resource_tags WHERE tag_id = {tag_id}
    resources = curr.fetchall()
    curr.close()
    return resources


def search_resources(tags, conn):
    tag_search = format_search(tags)
    cur = conn.cursor()
    cur.execute(
        "SELECT resources.id, create_date, resources.title, resources.link, resources.descr, array_agg(tags.title) as tags "
        "FROM resources "
        "LEFT JOIN resource_tags ON resources.id = resource_tags.resource_id "
        "LEFT JOIN tags ON resource_tags.tag_id = tags.id "
        f"WHERE tags.title IN{tag_search} OR resources.title IN {tag_search}"
        "GROUP BY resources.id "
        "ORDER BY create_date DESC;"
    )
    resources = cur.fetchall()
    return resources


def format_search(tags):
    tags = str(tags)
    tags = tags.split(" ")
    tag_search = "("
    for tag in tags:
        tag_search = tag_search + "'" + tag + "'"
        tag_search = tag_search + ","
    tag_search = tag_search[0:-1]
    tag_search = tag_search + ")"
    return tag_search
