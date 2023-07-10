import unittest
import os
import psycopg2
import testing.postgresql
import frontend.helper as h
from sqlalchemy import create_engine
import psycopg2


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
        ("tag1", "descr"),
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
    cursor.close()
    conn.commit()
    conn.close()

Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=True,
                                                  on_initialized=handler)

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
        self.assertTrue(h.table_exists(self.db, 'tags'))
        self.assertTrue(h.table_exists(self.db, 'resources'))
        self.assertFalse(h.table_exists(self.db, 'fake'))

    def test_add_to_res(self):
        title = "Test"
        link = "this_is_example"
        descr = "TestDescr"

        cur = self.db.cursor()

        # call the function
        h.add_to_resources(title, link, descr,self.db)

        # check results of output
        cur = self.db.cursor()
        results = cur.execute("SELECT * FROM resources")
        data = cur.fetchall()
        newest_item = data[-1]
        self.assertEqual(newest_item[2],title)
        self.assertEqual(newest_item[3],link)
        self.assertEqual(newest_item[4],descr)

    def test_add_to_tags(self):
        title = "Test"
        descr = "TestDescr"

        cur = self.db.cursor()

        # call the function
        h.add_to_tags(title, descr,self.db)

        # check results of output
        cur = self.db.cursor()
        results = cur.execute("SELECT * FROM tags")
        data = cur.fetchall()
        newest_item = data[-1]
        self.assertEqual(newest_item[1],title)
        self.assertEqual(newest_item[2],descr)



        




        



