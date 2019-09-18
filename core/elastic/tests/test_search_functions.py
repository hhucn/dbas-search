import unittest

from core.v1.search import create_connection, get_all_statements_with_value


class TestContentList(unittest.TestCase):

    def setUp(self):
        self.es = create_connection()

    def test_exception_is_thrown_if_es_is_down(self):
        with self.assertRaises(AttributeError):
            get_all_statements_with_value(None, 1, "Coconut")
