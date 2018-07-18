import time
import unittest

from core.v2.elastic.interface.es_interface import ESInterface


class TestESInterfaceResults(unittest.TestCase):
    def setUp(self):
        self.interface = ESInterface(index="coconut", file="request.sql")
        self.interface.initialize_new_index()
        time.sleep(3)

    def test_get_source_result_empty(self):
        res = self.interface.get_source_result(field="text:", text="Foo")
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
