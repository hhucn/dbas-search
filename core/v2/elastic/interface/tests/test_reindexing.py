import time
import unittest

from core.v2.elastic.interface.es_interface import ESInterface
from core.v2.elastic.interface.tests.test_interface_results import id_generator
from core.v2.elastic.mechanics.es_connector import ESConnector
from core.v2.elastic.queries.es_query import ESQuery


class TestReindexing(unittest.TestCase):

    def setUp(self):
        self.id = id_generator(100)
        self.interface = ESInterface(index=self.id, file="request.sql")
        self.interface.initialize_new_index()
        time.sleep(3)

    def test_reindex_from_to(self):
        id_2 = id_generator(100)
        es_client = ESConnector(index=id_2)
        es_client.create_index()
        self.assertTrue(self.interface.es.indices.exists(index=id_2))
        self.interface.reindex_to(destination=id_2)
        time.sleep(2)
        res = es_client.search_with(query=ESQuery(field="text", text="Cat", fuzziness=1).semantic_search_query())
        time.sleep(3)
        res = res.get("hits").get("hits")
        self.assertIsNotNone(res)
        self.assertNotEqual(len(res), 0)
