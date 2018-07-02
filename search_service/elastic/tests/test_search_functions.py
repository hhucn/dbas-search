import time
import unittest

from search_service.database.query_with_graphql import query_start_point_issue_of_statement, send_request_to_graphql
from search_service.elastic.search import create_connection, get_all_statements_with_value, get_suggestions, get_edits, \
    get_duplicates_or_reasons


class TestContentList(unittest.TestCase):

    def setUp(self):
        time.sleep(6)
        self.es = create_connection()

    def test_get_suggestions_not_empty(self):
        """
        Test if get_suggestions has a result for any position to a
        given search-word which leads to a search result.

        :return:
        """
        res = get_suggestions(self.es, 2, "cat", True)
        self.assertNotEqual(len(res), 0)

        res = get_suggestions(self.es, 2, "cat", False)
        self.assertNotEqual(len(res), 0)

    def test_get_suggestions_is_empty(self):
        """
        Test if get_suggestions has no result for any position to a
        given search-word which leads to no search result.

        :return:
        """
        res = get_suggestions(self.es, 2, "coconut", True)
        self.assertEqual(len(res), 0)

        res = get_suggestions(self.es, 2, "coconut", False)
        self.assertEqual(len(res), 0)

    def test_get_suggestions_contains_search_word(self):
        """
        Test if suggestion really contains search word.

        :return:
        """
        res = get_suggestions(self.es, 2, "cat", True)
        self.assertIn("cat", str(res))

        res = get_suggestions(self.es, 2, "cat", False)
        self.assertIn("cat", str(res))

    def test_get_matching_edits_is_empty(self):
        """
        Test if get matching edits has no result.
        Todo: There is currently no edit case in the database. Therefore add one and test it

        :return:
        """

        res = get_edits(self.es, 2, 48, "cat")
        self.assertEqual(len(res), 0)

    def test_get_duplicates_or_reasons_not_empty(self):
        """
        Test if get_duplicates_or_reasons is not empty for a given search-word
        leading to a search-result.

        :return:
        """

        res = get_duplicates_or_reasons(self.es, 2, 2, "we should get a cat")
        self.assertNotEqual(len(res), 0)

    def test_get_duplicate_or_reasons_is_empty(self):
        """
        Test if get_duplicates_or_reasons is empty for a given search-word
        leading to no search-result.

        :return:
        """
        res = get_duplicates_or_reasons(self.es, 2, 2, "coconut")
        self.assertEqual(len(res), 0)

    def test_get_duplicate_or_reasons_does_not_contain_target_statement(self):
        """
        Test if get_duplicates_or_reasons doesn't list the target statement
        in its result list.

        :return:
        """
        res = get_duplicates_or_reasons(self.es, 2, 2, "we should get a cat")
        for i in res:
            self.assertNotEqual(i["statement_uid"], 2)

    def test_get_all_statements_with_value_not_empty(self):
        """
        Test if get_all_statements_with_value is not empty to a given
        value which leads to a search-result.

        :return:
        """
        res = get_all_statements_with_value(self.es, 2, "we")
        self.assertNotEqual(len(res), 0)

    def test_get_all_statements_with_value_is_empty(self):
        """
        Test if get_all_statements_with_value is empty to a given
        value which leads to no search-result.

        :return:
        """
        res = get_all_statements_with_value(self.es, 2, "coconut")
        self.assertEqual(len(res), 0)

    def test_get_all_statements_with_value_contains_value(self):
        """
        Test if get_all_statements_with_value really contains the value
        in its result-list.

        :return:
        """
        res = get_all_statements_with_value(self.es, 2, "we")
        self.assertIn("we", str(res))

        self.es = create_connection()

    def test_query_start_point_issue_of_statement(self):
        """
        Test if query_start_point_issue_of_statement returns data.

        :return:
        """
        query = query_start_point_issue_of_statement(1)
        res = send_request_to_graphql(query)
        self.assertGreater(len(res), 0)

    def test_exception_is_thrown_if_es_is_down(self):
        with self.assertRaises(AttributeError):
            get_all_statements_with_value(None, 1, "Coconut")
