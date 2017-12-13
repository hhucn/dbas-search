import unittest

from search_service.database_handling.query_with_graphql import graphql_query, \
    query_all_users_nicknames_with_issues, get_uid_of_issue, \
    get_length_of_json, query_all_data_by_uid


class TestQueries(unittest.TestCase):
    def test_all_users_with_issues_length_is_five(self):
        query = query_all_users_nicknames_with_issues()
        response = graphql_query(query)
        data_length = get_length_of_json(response.get("issues"))
        self.assertEqual(data_length, 5)

    def test_cat_or_uid_is_two(self):
        uid = get_uid_of_issue("cat-or-dog")
        self.assertEqual(uid, 2)

    def test_make_the_world_better_uid_is_three(self):
        uid = get_uid_of_issue("make-the-world-better")
        self.assertEqual(uid, 3)

    def test_elektroautos_uid_is_four(self):
        uid = get_uid_of_issue("elektroautos")
        self.assertEqual(uid, 4)


class TestModifiedQuerie(unittest.TestCase):
    def test_response_is_a_start_point(self):
        query = query_all_data_by_uid(2, True)
        response = graphql_query(query)
        for i in range(0, get_length_of_json(response.get("statements"))):
            is_start_point = response.get("statements")[0].get("isStartpoint")
            self.assertTrue(is_start_point)

    def test_response_is_not_a_start_point(self):
        query = query_all_data_by_uid(2, False)
        response = graphql_query(query)
        for i in range(0, get_length_of_json(response.get("statements"))):
            is_start_point = response.get("statements")[0].get("isStartpoint")
            self.assertFalse(is_start_point)


class TestLanguageOfIssue(unittest.TestCase):
    def test_cat_and_dog_is_english(self):
        query_startpoint = query_all_data_by_uid(2, True)
        query_not_startpoint = query_all_data_by_uid(2, False)

        response_startpoint = graphql_query(query_startpoint)
        response_not_startpoint = graphql_query(query_not_startpoint)

        language_1 = response_startpoint.get("statements")[0].get("issues").get("langUid")
        language_2 = response_not_startpoint.get("statements")[0].get("issues").get("langUid")

        self.assertEqual(language_1, language_2)
        self.assertEqual(language_1, 1)
        self.assertEqual(language_2, 1)

    def e_autos_are_german(self):
        query_startpoint = query_all_data_by_uid(4, True)
        query_not_startpoint = query_all_data_by_uid(4, False)

        response_startpoint = graphql_query(query_startpoint)
        response_not_startpoint = graphql_query(query_not_startpoint)

        language_1 = response_startpoint.get("statements")[0].get("issues").get("langUid")
        language_2 = response_not_startpoint.get("statements")[0].get("issues").get("langUid")

        self.assertEqual(language_1, language_2)
        self.assertEqual(language_1, 2)
        self.assertEqual(language_2, 2)
