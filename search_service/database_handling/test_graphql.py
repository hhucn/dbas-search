import unittest

from search_service.database_handling.query_with_graphql import send_request_to_graphql, query_issue_id, \
    query_all_uid, query_language_of_issue, \
    query_data_of_issue


class TestRequest(unittest.TestCase):

    def test_empty_query_has_response(self):
        response = send_request_to_graphql("query{}")
        self.assertIsNotNone(response)

    def test_query_id_of_issue_by_slug_returns_id(self):
        query = query_issue_id("town-has-to-cut-spending")
        response = send_request_to_graphql(query)
        self.assertIsNotNone(response)

    def test_query_all_ids_has_response(self):
        query = query_all_uid()
        response = send_request_to_graphql(query)
        self.assertIsNotNone(response)

    def test_if_there_are_five_issues(self):
        query = query_all_uid()
        response = send_request_to_graphql(query)
        self.assertGreaterEqual(len(response.get("issues")), 5)

    def test_language_of_town_has_to_cut_spending_is_english(self):
        query = query_language_of_issue(2)
        response = send_request_to_graphql(query).get("issue").get("languages").get("uiLocales")
        self.assertEqual(response, "en")

    def test_language_pferdehuhn_is_german(self):
        uid = send_request_to_graphql(query_issue_id("pferdehuhn")).get("issue").get("uid")
        query = query_language_of_issue(int(uid))
        response = send_request_to_graphql(query).get("issue").get("languages").get("uiLocales")
        self.assertEqual(response, "de")

    def test_len_of_town_has_to_cut_spending_is_greater_or_equals_29(self):
        query_uid = query_issue_id("town-has-to-cut-spending")
        uid = send_request_to_graphql(query_uid).get("issue").get("uid")
        query_datas = query_data_of_issue(uid)
        response = send_request_to_graphql(query_datas)
        len_response = len(response.get("statements"))
        self.assertGreaterEqual(len_response, 29)
