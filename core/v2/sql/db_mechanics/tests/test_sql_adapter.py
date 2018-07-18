import unittest

from core.v2.sql.db_mechanics.dbconnector import DBConnector
from core.v2.sql.sql_commands.sql_adapter import SQLAdapter


class TestSQLAdapter(unittest.TestCase):
    def test_adapter_reads_sql_file(self):
        adapter = SQLAdapter(file='request.sql')
        self.assertIsNotNone(adapter.read_file())

    def test_database_gets_result_with_query_read_by_the_adapter(self):
        adapter = SQLAdapter(file='request.sql')
        database = DBConnector()
        res = database.query(adapter.read_file())
        self.assertIsNotNone(res)
        database.close_all()
