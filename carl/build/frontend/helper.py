import os
import psycopg2

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


def add_to_resources(title, link, descr, conn, tag):
    
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
    cur.execute(
        "SELECT id FROM resources ORDER BY create_date DESC LIMIT 1;"
    )
    res_id = cur.fetchall()
    res_id = res_id[0]
    cur.close()
    cur = conn.cursor()
    cur.execute(
        f"SELECT id FROM tags WHERE title IN ('{tag}');"
    )
    tag_id = cur.fetchall()

    cur.execute(
        "INSERT INTO restag (resource_id, tag_id)" "VALUES (%s,%s)",
        (res_id,tag_id)
    )
    
    cur.close()
    
    


def add_to_tags(title, descr,conn):
    #conn = get_db_connection()
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
    #conn.close()

def add_to_projects(title, descr,conn):
    #conn = get_db_connection()
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
    #conn.close()

