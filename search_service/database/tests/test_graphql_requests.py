import unittest

from search_service.database.query_with_graphql import send_request_to_graphql, query_issue_id, \
    query_all_uid, query_language_of_issue, \
    query_data_of_issue, get_uid_of_issue


class TestGraphQLRequest(unittest.TestCase):

    def test_for_valid_request_with_missing_envs(self):
        """
        Test if the parameters are set properly with missing envs.

        :return:
        """
        response = send_request_to_graphql("query{}", "", "", "")
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

    def test_if_there_are_five_issues(self):
        """
        Test if there more the five issues.

        :return:
        """
        query = query_all_uid()
        response = send_request_to_graphql(query)
        self.assertGreaterEqual(len(response.get("issues")), 5)

    def test_language_of_town_has_to_cut_spending_is_english(self):
        """
        Test language of town-has-to-cut-spending is english.

        :return:
        """
        query = query_language_of_issue(2)
        response = send_request_to_graphql(query).get("issue").get("languages").get("uiLocales")
        self.assertEqual(response, "en")

    def test_len_of_town_has_to_cut_spending_is_greater_or_equals_0(self):
        """
        Test if town-has-to-cut-spending has content.

        :return:
        """
        query_uid = query_issue_id("town-has-to-cut-spending")
        uid = send_request_to_graphql(query_uid).get("issue").get("uid")
        query_data = query_data_of_issue(uid)
        response = send_request_to_graphql(query_data)
        len_response = len(response.get("statements"))
        self.assertGreaterEqual(len_response, 0)

    def test_uid_of_cat_or_dog_is_2(self):
        """
        Test if cat-or-dog uid is 2.

        :return:
        """
        slug = "cat-or-dog"
        self.assertEqual(get_uid_of_issue(slug), 2)
