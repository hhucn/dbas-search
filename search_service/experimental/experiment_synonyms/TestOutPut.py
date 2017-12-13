import unittest

from search_service.elastic.elastic_search import create_elastic_search_client


class TestOutPut(unittest.TestCase):
    '''
    This may solve the problem of the loosing connection and the high requests
    '''

    def setUp(self):
        self.client = create_elastic_search_client()

    def test_es_ist_da(self):
        self.assertTrue(self.client.ping())
