from build.frontend.helper import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute(
    "drop table if exists project_resources, project_tags, resource_tags, resources, tags, projects;"
)

conn.commit()
cur.close()
conn.close()
