import unittest

from core.database.query_with_graphql import send_request_to_graphql, query_issue_id, \
    query_all_uid


class TestGraphQLRequest(unittest.TestCase):

    def test_for_valid_request_with_missing_envs(self):
        """
        Test if the parameters are set properly with missing envs.

        :return:
        """
        response = send_request_to_graphql("query{}", "", "", 0)
        self.assertIsNotNone(response)

    def test_empty_query_has_response(self):
        """
        Test if a empty query leads to a response of GraphQl.

        :return:
        """
        response = send_request_to_graphql("query{}")
        self.assertIsNotNone(response)

    def test_query_id_of_issue_by_slug_returns_id(self):
        """
        Test if query by slug leads to a result.

        :return:
        """
        query = query_issue_id("town-has-to-cut-spending")
        response = send_request_to_graphql(query)
        self.assertIsNotNone(response)

    def test_query_all_ids_has_response(self):
        """
        Test if GraphQl returns all uid of active issues.

        :return:
        """
        query = query_all_uid()
        response = send_request_to_graphql(query)
        self.assertIsNotNone(response)
