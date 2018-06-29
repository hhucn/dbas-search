"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
import unittest

from search_service.database.query_with_graphql import get_uid_of_issue
from search_service.elastic.search import create_connection, INDEX_NAME, \
    get_matching_statements, get_suggestions, get_availability


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.client = create_connection()

    def test_connection_is_alive(self):
        self.assertTrue(self.client.ping())
