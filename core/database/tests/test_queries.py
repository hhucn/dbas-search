import unittest

from core.database.query_with_graphql import query_issue_id, \
    query_language_of_issue, \
    query_data_of_issue, query_start_point_issue_of_statement


class TestGraphQLQueries(unittest.TestCase):

    def test_query_issue_id(self):
        """
        Test if slug is set properly in uid query.

        :return:
        """
        query = query_issue_id(2)
        self.assertIn('issue(slug: "2")', query)

    def test_query_language(self):
        """
        Test if uid is set properly in language query.

        :return:
        """
        query = query_language_of_issue(2)
        self.assertIn("issue(uid: 2)", query)

    def test_query_data(self):
        """
        Test if issueUid is set properly in data query.

        :return:
        """
        query = query_data_of_issue(2)
        self.assertIn("statements(issueUid: 2)", query)

    def test_query_data_of_issue(self):
        """
        Test if issueUid is set properly.

        :return:
        """
        query = query_data_of_issue(2)
        self.assertIn("statements(issueUid: 2)", query)

    def test_query_start_point_issue_of_statement(self):
        """
        Test if uid is set properly.

        :return:
        """
        query = query_start_point_issue_of_statement(2)
        self.assertIn("statement(uid: 2)", query)
