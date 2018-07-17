import unittest

from core import INDEX_NAME_2
from core.v2.elastic.mechanics.es_connector import ESConnector


class TestConnector(unittest.TestCase):
    def setUp(self):
        self.conn = ESConnector(index="banana")

    def test_default_index_name(self):
        self.assertEqual(ESConnector().index_name, INDEX_NAME_2)

    def test_new_index_name(self):
        self.assertEqual(ESConnector(index="foo").index_name, "foo")

    def test_create_index(self):
        self.conn.create_index()
        self.assertTrue(self.conn.index_exists())

    def test_delete_index(self):
        self.conn.delete_index()
        self.assertFalse(self.conn.index_exists())
