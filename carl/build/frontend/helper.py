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
        "VALUES (%s, %s, %s) RETURNING id",
        (title, link, descr),
    )
    resource_id = cur.fetchone()[0]
    conn.commit()
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
        SELECT resources.id, create_date, resources.title, resources.link, resources.descr, array_agg(tags.title) as tags
        FROM resources
        LEFT JOIN resource_tags ON resources.id = resource_tags.resource_id
        LEFT JOIN tags ON resource_tags.tag_id = tags.id
        WHERE resources.id=%s
        GROUP BY resources.id
        """,
            (id,),
        )
        resource = cur.fetchone()
    return resource


def update_resource(id, title, link, descr, tags, conn):
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


def add_to_tags(title, descr, conn):
    cur = conn.cursor()

    # Create table if it does not exist.
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
        return False

    # If the tag does not exist, create it and return True.
    cur.execute(
        "INSERT INTO tags (title, descr) VALUES (%s, %s)",
        (title, descr),
    )
    conn.commit()
    cur.close()
    return True
    # conn.close()


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
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE tags SET title=%s, descr=%s WHERE id=%s",
            (title, descr, id),
        )
    conn.commit()


def add_to_projects(title, descr, conn):
    # conn = get_db_connection()
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
    # conn.close()


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
    cur.execute(
        "SELECT DISTINCT 0 as id, title, descr FROM projects ORDER BY title ASC;"
    )
    projects = cur.fetchall()
    cur.close()
    return projects


def get_resources(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT resources.id, create_date, resources.title, resources.link, resources.descr, array_agg(tags.title) as tags "
        "FROM resources "
        "LEFT JOIN resource_tags ON resources.id = resource_tags.resource_id "
        "LEFT JOIN tags ON resource_tags.tag_id = tags.id "
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
