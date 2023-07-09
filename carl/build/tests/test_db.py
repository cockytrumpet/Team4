import unittest
import os
import psycopg2
import testing.postgresql
import frontend.helper as h
from sqlalchemy import create_engine
import psycopg2

class Test(unittest.TestCase):

    def setUp(self):
        # create a new PostgreSQL server
        self.postgresql = testing.postgresql.Postgresql()
        # connect to PostgreSQL
        engine = create_engine(self.postgresql.url())
        # use driver
        self.db = psycopg2.connect(**self.postgresql.dsn())
        # initialize database with schema and tables
        with self.db.cursor() as cur:
            cur.execute(self.read_file('./tests/init.sql'))


    def read_file(self,path):
        '''Reads in and returns the contents of a file'''
        with open(path, 'r') as f:
            return f.read()
    
    def tearDown(self):
        self.db.close()
        self.postgresql.stop()

    def test_table_exists(self):
        self.assertTrue(h.table_exists(self.db, 'tags'))
        self.assertFalse(h.table_exists(self.db, 'fake'))


