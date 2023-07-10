from build.frontend.helper import get_db_connection

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
