import unittest

from core import STATEMENT_INDEX
from core.v2.elastic.mechanics.es_connector import ESConnector


class TestMappingSetting(unittest.TestCase):
    def setUp(self):
        self.conn = ESConnector(index=STATEMENT_INDEX)

    def test_get_mapping(self):
        resp = self.conn.es.indices.get_mapping(index=STATEMENT_INDEX)
        self.assertIsNotNone(resp)

    def test_get_settings(self):
        resp = self.conn.es.indices.get_settings(index=STATEMENT_INDEX)
        self.assertIsNotNone(resp)
