from build.frontend.helper import get_db_connection

conn = get_db_connection()
cur = conn.cursor()


def print_tables(cur):
    cur.execute(
        "select * from information_schema.tables where table_schema='public';"
    )
    for table in cur.fetchall():
        cur.execute(f"select * from {table[2]};")
        print(f"[{table[2]}]")
        for line in cur.fetchall():
            print(f"  {line}")


if __name__ == "__main__":
    print_tables(cur)
