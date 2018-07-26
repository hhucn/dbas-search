import random
import string
import unittest

from core import STATEMENT_INDEX
from core.v2.elastic.mechanics.es_connector import ESConnector


def id_generator(size):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(size))


class TestConnector(unittest.TestCase):
    def setUp(self):
        self.index_name = id_generator(100)
        self.conn = ESConnector(index=self.index_name)

    def test_default_index_name(self):
        self.assertEqual(ESConnector().index_name, STATEMENT_INDEX)

    def test_new_index_name(self):
        self.assertEqual(ESConnector(index="foo").index_name, "foo")

    def test_create_index_and_delete_index(self):
        self.assertEqual(self.conn.index_name, self.index_name)
        self.conn.create_index()
        self.assertTrue(self.conn.index_exists())
        self.assertEqual(self.conn.index_name, self.index_name)
        self.conn.delete_index()
        self.assertFalse(self.conn.index_exists())
