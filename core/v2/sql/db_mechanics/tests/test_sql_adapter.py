import unittest

from core.v2.sql.db_mechanics.database import Database
from core.v2.sql.db_mechanics.sql_adapter import SQLAdapter


class TestSQLAdapter(unittest.TestCase):
    def test_adapter_reads_sql_file(self):
        ad = SQLAdapter(path='../sql_commands/request.sql')
        self.assertIsNotNone(ad.read_file())

    def test_database_gets_result_with_query_read_by_the_adapter(self):
        ad = SQLAdapter(path='../sql_commands/request.sql')
        db = Database()
        res = db.query(ad.read_file())
        self.assertIsNotNone(res)
        db.close_all()
