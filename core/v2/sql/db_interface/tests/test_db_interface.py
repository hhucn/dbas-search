import unittest

from core.v2.sql.db_interface.db_interface import DBInterface


class TestDBInterface(unittest.TestCase):
    def test_if_the_db_interface_returns_results_1(self):
        interface = DBInterface(path='../sql_commands/request.sql')
        result = interface.query_data_with_sql()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

    def test_if_the_db_interface_returns_results_2(self):
        interface = DBInterface(path='../sql_commands/request.sql')
        result = interface.query_data_with_sql()
        for res in result:
            self.assertIsNotNone(res)
            self.assertIsInstance(res, dict)
