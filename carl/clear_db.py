from build.frontend.app import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute("drop table if exists resources, tags, projects;")

conn.commit()
cur.close()
conn.close()
