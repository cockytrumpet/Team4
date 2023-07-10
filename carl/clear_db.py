import sys
sys.path.append('/workspaces/Team4/carl/build/frontend/')

from build.frontend.app import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute("drop table if exists resources, tags, projects, resource_tags;")

conn.commit()
cur.close()
conn.close()
