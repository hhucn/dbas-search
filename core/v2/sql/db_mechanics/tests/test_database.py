import unittest

from core.v2.sql.db_mechanics.dbconnector import DBConnector
from core.v2.sql.sql_commands.sql_adapter import SQLAdapter


class TestDatabase(unittest.TestCase):

    def test_connection_up_and_down(self):
        db = DBConnector()
        self.assertFalse(db.conn.closed)  # database connection is online
        self.assertFalse(db.curs.closed)  # cursor connection is online
        db.close_all()
        self.assertTrue(db.curs.closed)  # database connection is down
        self.assertTrue(db.curs.closed)  # database connection is down

    def test_for_results_as_real_dict_tuples(self):
        db = DBConnector()
        res = db.query(SQLAdapter(file='request.sql').read_file())
        self.assertIsNotNone(res)
        for r in res:
            for desc in db.curs.description:
                self.assertIsNotNone(r[desc.name])
