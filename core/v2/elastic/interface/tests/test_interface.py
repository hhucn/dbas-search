import time
import unittest

from core import INDEX_NAME_2
from core.v2.elastic.interface.es_interface import ESInterface
from core.v2.elastic.queries.es_query import ESQuery


class TestInterface(unittest.TestCase):
    def setUp(self):
        self.interface = ESInterface(index="banana", file="request.sql")

    def test_default_values(self):
        interface = ESInterface()
        self.assertEqual(interface.index_name, INDEX_NAME_2)
        self.assertEqual(interface.file, None)

    def test_non_default_values(self):
        self.assertEqual(self.interface.index_name, "banana")
        self.assertEqual(self.interface.file, "request.sql")

    def test_init_new_index_and_query(self):
        self.interface.initialize_new_index()
        query = ESQuery(field="text:", text="Cat", fuzziness=2).sem_query()
        time.sleep(5)
        res = self.interface.search_with(query=query).get("hits").get("hits")
        self.assertGreater(len(res), 0)
