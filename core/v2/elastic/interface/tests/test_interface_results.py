import random
import string
import time
import unittest

from core.v2.elastic.interface.es_interface import ESInterface


def id_generator(size):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(size))


class TestESInterfaceResults(unittest.TestCase):
    def setUp(self):
        self.interface = ESInterface(index=id_generator(100), file="request.sql")
        self.interface.initialize_new_index()
        time.sleep(3)

    def test_get_source_result_empty_1(self):
        res = self.interface.get_source_result(field="text", text="Coconut")
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 0)

    def test_get_source_result_empty_2(self):
        res = self.interface.get_source_result(field="text", text="Coconut")
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 0)

    def test_get_source_result_empty_3(self):
        res = self.interface.get_source_result(field="text", text="coCocNut")
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 0)

    def test_get_source_result_not_empty_1(self):
        res = self.interface.get_source_result(field="text", text="Cat")
        self.assertIsNotNone(res)
        self.assertNotEqual(len(res), 0)

    def test_get_source_result_not_empty_2(self):
        res = self.interface.get_source_result(field="author.nickname", text="anonymous")
        self.assertIsNotNone(res)
        self.assertNotEqual(len(res), 0)
