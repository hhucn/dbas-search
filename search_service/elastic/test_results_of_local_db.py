import unittest

import requests

from search_service.elastic.search import create_connection


class TestDuplicateReasons(unittest.TestCase):
    def setUp(self):
        self.client = create_connection()

    def test_statement_not_in_results1(self):
        r = requests.get('http://localhost:5000/duplicates_reasons?id=4&statement_uid=58')
        self.assertNotIn('optimal', r.text)

    def test_statement_not_in_results2(self):
        r = requests.get('http://localhost:5000/duplicates_reasons?id=4&statement_uid=58&search=optimal')
        self.assertEqual(0, len(r.json().get("result")))
