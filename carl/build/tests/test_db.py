import unittest
import os
import psycopg2
import testing.postgresql
import frontend.helper as h
from sqlalchemy import create_engine


def handler(postgresql):
    conn = psycopg2.connect(**postgresql.dsn())
    cursor = conn.cursor()

    # Tag Table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS tags (id serial PRIMARY KEY,"
        "title varchar (150) NOT NULL,"
        "descr text);"
    )
    cursor.execute(
        "INSERT INTO tags (title, descr)" "VALUES (%s, %s)",
        ("test_tag1", "descr"),
    )
    cursor.execute(
        "INSERT INTO tags (title, descr)" "VALUES (%s, %s)",
        ("test_tag2", "descr2"),
    )
    # Resources Table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS resources (id serial PRIMARY KEY,"
        "create_date DATE DEFAULT (CURRENT_DATE),"
        "title varchar (150) NOT NULL,"
        "link text,"
        "descr text);"
    )
    cursor.execute(
        "INSERT INTO resources (title, link, descr)" "VALUES (%s, %s, %s)",
        (
            "Stack Overflow Article",
            "https://stackoverflow.com/questions/20461030/current-date-curdate-not-working-as-default-date-value",
            "Current Date Function",
        ),
    )
    cursor.execute(
        "INSERT INTO resources (title, link, descr)" "VALUES (%s, %s, %s)",
        (
            "Another Article",
            "link",
            "another article description",
        ),
    )
    cursor.close()
    conn.commit()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS resource_tags (id serial PRIMARY KEY,"
        "resource_id integer,"
        "tag_id integer,"
        "FOREIGN KEY (resource_id) REFERENCES resources (id),"
        "FOREIGN KEY (tag_id) REFERENCES tags (id));"
    )
    cursor.execute("SELECT DISTINCT id FROM resources")
    resource_ids = cursor.fetchall()
    cursor.execute("SELECT DISTINCT id FROM tags")
    tag_ids = cursor.fetchall()

    for res_id in resource_ids:
        for tag_id in tag_ids:
            cursor.execute(
                "INSERT INTO resource_tags (resource_id, tag_id)"
                "VALUES (%s, %s)",
                (res_id, tag_id),
            )

    cursor.close()
    conn.commit()
    conn.close()


Postgresql = testing.postgresql.PostgresqlFactory(
    cache_initialized_db=True, on_initialized=handler
)

# Generate Postgresql class which shares the generated database


class Test(unittest.TestCase):
    def setUp(self):
        # create a new PostgreSQL server
        self.postgresql = Postgresql()
        # connect to PostgreSQL
        engine = create_engine(self.postgresql.url())
        # use driver
        self.db = psycopg2.connect(**self.postgresql.dsn())

    def tearDown(self):
        self.db.close()
        self.postgresql.stop()

    def test_table_exists(self):
        self.assertTrue(h.table_exists(self.db, "tags"))
        self.assertTrue(h.table_exists(self.db, "resources"))
        self.assertFalse(h.table_exists(self.db, "fake"))

    def test_add_to_res(self):
        title = "Test"
        link = "this_is_example"
        descr = "TestDescr"

        cur = self.db.cursor()

        # call the function
        h.add_to_resources(title, link, descr, self.db)

        # check results of output
        cur = self.db.cursor()
        results = cur.execute("SELECT * FROM resources ORDER BY id ASC")
        # items are not necessarily returned in order - cannot assume it's returned in order of creation
        data = cur.fetchall()
        newest_item = data[-1]

        if link[:5].lower() != "http":
            new_link = "http://" + link

        self.assertEqual(newest_item[2], title)
        self.assertEqual(newest_item[3], new_link)
        self.assertEqual(newest_item[4], descr)

        message = h.add_to_resources(title, link, descr, self.db)
        self.assertEqual(message[0], "error")

    def test_add_to_tags(self):
        title = "Test"
        descr = "TestDescr"

        cur = self.db.cursor()

        # call the function
        h.add_to_tags(title, descr, self.db)

        # check results of output
        cur = self.db.cursor()
        results = cur.execute("SELECT * FROM tags ORDER BY id ASC")
        # items are not necessarily returned in order - cannot assume it's returned in order of creation
        data = cur.fetchall()
        newest_item = data[-1]
        self.assertEqual(newest_item[1], title)
        self.assertEqual(newest_item[2], descr)

    def test_get_tagged_resources(self):
        # test_tag2
        cur = self.db.cursor()
        cur.execute("SELECT * FROM tags WHERE title = 'test_tag2'")
        tag_ids = cur.fetchall()
        tag_id = tag_ids[0][0]

        results = h.get_tagged_resources(tag_id, self.db)
        # we expect that we should get two resources
        cur.execute(
            f"SELECT resource_id FROM resource_tags WHERE tag_id = {tag_id} ORDER BY resource_id"
        )
        resource_ids = cur.fetchall()
        self.assertEqual(results[0][0], resource_ids[0][0])
        self.assertEqual(results[0][0], resource_ids[0][0])
