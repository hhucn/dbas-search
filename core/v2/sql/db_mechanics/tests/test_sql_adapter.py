import unittest

from core.v2.sql.db_mechanics.dbconnector import DBConnector
from core.v2.sql.sql_commands.sql_adapter import SQLAdapter


class TestSQLAdapter(unittest.TestCase):
    def test_adapter_reads_sql_file(self):
        ad = SQLAdapter(file='request.sql')
        self.assertIsNotNone(ad.read_file())

    def test_database_gets_result_with_query_read_by_the_adapter(self):
        ad = SQLAdapter(file='request.sql')
        db = DBConnector()
        res = db.query(ad.read_file())
        self.assertIsNotNone(res)
        db.close_all()
