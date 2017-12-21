import unittest

from search_service.database_handling.query_with_graphql import graphql_query, query_issue_id_by_issue_slug, \
    query_all_uids, query_language_of_issue_by_uid, \
    query_every_datas_from_active_issue


class TestRequest(unittest.TestCase):

    def test_empty_query_has_response(self):
        response = graphql_query("query{}")
        self.assertIsNotNone(response)

    def test_query_id_of_issue_by_slug_returns_id(self):
        query = query_issue_id_by_issue_slug("town-has-to-cut-spending")
        response = graphql_query(query)
        self.assertIsNotNone(response)

    def test_query_all_ids_has_response(self):
        query = query_all_uids()
        response = graphql_query(query)
        self.assertIsNotNone(response)

    def test_if_there_are_five_issues(self):
        query = query_all_uids()
        response = graphql_query(query)
        self.assertGreaterEqual(len(response.get("issues")), 5)

    def test_language_of_town_has_to_cut_spending_is_english(self):
        query = query_language_of_issue_by_uid(2)
        response = graphql_query(query).get("issue").get("languages").get("uiLocales")
        self.assertEqual(response, "en")

    def test_language_pferdehuhn_is_german(self):
        uid = graphql_query(query_issue_id_by_issue_slug("pferdehuhn")).get("issue").get("uid")
        query = query_language_of_issue_by_uid(int(uid))
        response = graphql_query(query).get("issue").get("languages").get("uiLocales")
        self.assertEqual(response, "de")

    def test_len_of_town_has_to_cut_spending_is_greater_or_equals_29(self):
        query_uid = query_issue_id_by_issue_slug("town-has-to-cut-spending")
        uid = graphql_query(query_uid).get("issue").get("uid")
        query_datas = query_every_datas_from_active_issue(uid)
        response = graphql_query(query_datas)
        len_response = len(response.get("statements"))
        self.assertGreaterEqual(len_response, 29)
