import unittest

from core.elastic.search import create_connection


class TestConnection(unittest.TestCase):

    def setUp(self):
        self.client = create_connection()

    def test_connection_is_alive(self):
        """
        Test if the Elasticsearch is available.

        :return:
        """
        self.assertTrue(self.client.ping())
