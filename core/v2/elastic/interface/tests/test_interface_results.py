import random
import string
import time
import unittest

from core.v2.elastic.interface.es_interface import ESInterface
from core.v2.elastic.mechanics.es_connector import ESConnector
from core.v2.elastic.queries.es_query import ESQuery


def id_generator(size):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(size))


class TestESInterfaceResults(unittest.TestCase):
    def setUp(self):
        self.interface = ESInterface(index=id_generator(100), file="request.sql")
        self.interface.initialize_new_index()
        time.sleep(3)

    def test_get_source_result_empty_1(self):
        res = self.interface.get_source_result(field="text:", text="Foo")
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 0)

    def test_get_source_result_empty_2(self):
        res = self.interface.get_source_result(field="text:")
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 0)

    def test_get_source_result_empty_3(self):
        res = self.interface.get_source_result(field="text:", text="''")
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 0)

    def test_get_source_result_empty_4(self):
        res = self.interface.get_source_result(field="text:", text="")
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 0)

    def test_get_source_result_not_empty_1(self):
        res = self.interface.get_source_result(field="text:", text="Cat")
        self.assertIsNotNone(res)
        self.assertNotEqual(len(res), 0)

    def test_get_source_result_not_empty_2(self):
        res = self.interface.get_source_result(field="author.nickname", text="anonymous")
        self.assertIsNotNone(res)
        self.assertNotEqual(len(res), 0)

    def test_get_source_result_not_empty_3(self):
        res = self.interface.get_source_result(field="text:", text='""')
        self.assertIsNotNone(res)
        self.assertNotEqual(len(res), 0)

    def test_reindex_from_to(self):
        id_2 = id_generator(100)
        self.interface.es.indices.create(index=id_2)
        self.assertTrue(self.interface.es.indices.exists(index=id_2))
        self.interface.reindex_to(destination=id_2)
        es_client = ESConnector(index=id_2)
        res = es_client.search_with(query=ESQuery(field="text:", text="Cat", fuzziness=1).sem_query())
        res = res.get("hits").get("hits")
        self.assertIsNotNone(res)
        self.assertNotEqual(len(res), 0)
