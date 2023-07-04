from build.frontend.app import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute("truncate resources, tags;")  # add projects once that table exists

conn.commit()
cur.close()
conn.close()
