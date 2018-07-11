import unittest

from core.v2.sql.db_mechanics.database import Database
from core.v2.sql.db_mechanics.sql_adapter import SQLAdapter


class TestDatabase(unittest.TestCase):

    def test_connection_up_and_down(self):
        db = Database()
        self.assertFalse(db.conn.closed)  # database connection is online
        self.assertFalse(db.curs.closed)  # cursor connection is online
        db.close_all()
        self.assertTrue(db.curs.closed)  # database connection is down
        self.assertTrue(db.curs.closed)  # database connection is down

    def test_for_results_as_real_dict_tuples(self):
        db = Database()
        res = db.query(SQLAdapter(path='../sql_commands/request.sql').read_file())
        self.assertIsNotNone(res)
        for r in res:
            for desc in db.curs.description:
                self.assertIsNotNone(r[desc.name])
