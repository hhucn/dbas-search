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


class TestElasticDB(unittest.TestCase):
    def setUp(self):
        # by starting the service the database should be filled
        self.client = create_connection()

    def test_database_has_filled(self):
        data1 = self.client.get(index=INDEX_NAME, doc_type="json", id=0)
        data2 = self.client.get(index=INDEX_NAME, doc_type="json", id=42)
        self.assertIsNotNone(data1, data2)


class TestElasticResults(unittest.TestCase):
    def setUp(self):
        self.client = create_connection()

    def test_find_swimming_pool_in_town_has_to_cut_spending(self):
        uid = get_uid_of_issue("town-has-to-cut-spending")
        search_words = ["swimming pools", "SWIMMING POOLS", "SWIMIng Ploos", "swimming poos", "swimming", "swim",
                        "pool", "poo"]
        es = self.client
        if not get_availability():
            self.assertRaises(Exception("Elastic is not available"),
                              get_matching_statements(es, uid, search_words[0], True))

        else:
            for search_word in search_words:
                search_results = get_matching_statements(es, uid, search_word, True)
                self.assertIsNotNone(search_results)

                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertIn("we should close public swimming pools", search_results)
                self.assertNotIn("the city should reduce the number of street festivals.", search_results)

    def test_find_street_festival_in_town_has_to_cut_spending(self):
        uid = get_uid_of_issue("town-has-to-cut-spending")
        search_words = ["street festival", "StreEt FestiVal", "SSTREET FFESTIVAL", "STREET", "FESTIVAL",
                        "STRIIT FASTIVEL"]
        es = self.client
        if not get_availability():
            self.assertRaises(Exception("Elastic is not available"),
                              get_matching_statements(es, uid, search_words[0], False))

        else:
            for search_word in search_words:
                search_results = get_matching_statements(es, uid, search_word, False)
                self.assertIsNotNone(search_results)

                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertIn("every street festival is funded by large companies", search_results)
                self.assertIn("reducing the number of street festivals can save up to $50.000 a year", search_results)
                self.assertNotIn("the city should reduce the number of street festivals.", search_results)

    def test_find_special_words(self):
        uid = get_uid_of_issue("town-has-to-cut-spending")
        search_words = ["$50.000"]
        es = self.client
        if not get_availability():
            self.assertRaises(Exception("Elastic is not available"),
                              get_matching_statements(es, uid, search_words[0], False))

        else:
            for search_word in search_words:
                search_results = get_matching_statements(es, uid, search_word, False)
                self.assertIsNotNone(search_results)

                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertNotIn("every street festival is funded by large companies", search_results)
                self.assertIn("reducing the number of street festivals can save up to $50.000 a year", search_results)
                self.assertNotIn("the city should reduce the number of street festivals.", search_results)

    def test_correct_highlighting_in_town_has_to_cut_spending(self):
        uid = get_uid_of_issue("town-has-to-cut-spending")
        search_words = ["street festival", "StreEt FestiVal", "SSTREET FFESTIVAL"]
        es = self.client
        if not get_availability():
            self.assertRaises(Exception("Elastic is not available"),
                              get_matching_statements(es, uid, search_words[0], False))

        else:
            for search_word in search_words:
                search_results = get_matching_statements(es, uid, search_word, False)
                self.assertIsNotNone(search_results)

                self.assertIn("every <em>street</em> <em>festival</em> is funded by large companies", search_results)
                self.assertIn("reducing the number of <em>street</em> <em>festivals</em> can save up to $50.000 a year",
                              search_results)
                self.assertIn(
                    "<em>street</em> <em>festivals</em> attract many people, which will increase the citys income",
                    search_results)
                self.assertIn("the road closures force traffic chaos while <em>street</em> <em>festivals</em>",
                              search_results)
                self.assertIn("spending of the city for these <em>festivals</em> are higher than the earnings",
                              search_results)

    def test_english_synonyms_are_used(self):
        uid = get_uid_of_issue("town-has-to-cut-spending")
        search_words = ["yakusie"]
        es = self.client
        if not get_availability():
            self.assertRaises(Exception("Elastic is not available"),
                              get_matching_statements(es, uid, search_words[0], True))

        else:
            for search_word in search_words:
                search_results = get_matching_statements(es, uid, search_word, True)
                self.assertIsNotNone(search_results)
                self.assertIn("we should close public <em>swimming</em> <em>pools</em>", search_results)

    def test_german_synonyms_are_used(self):
        uid = get_uid_of_issue("pferdehuhn")
        search_words = ["fogel"]
        es = self.client
        if not get_availability():
            self.assertRaises(Exception("Elastic is not available"),
                              get_matching_statements(es, uid, search_words[0], True))

        else:
            for search_word in search_words:
                search_results = get_matching_statements(es, uid, search_word, True)
                self.assertIsNotNone(search_results)
                self.assertIn("das <em>Huhn</em> gewinnen w\u00fcrde", search_results)


class TestElasticSuggestions(unittest.TestCase):
    def setUp(self):
        self.client = create_connection()

    def test_suggestions_for_swimming_pool_in_town_has_to_cut_spending(self):
        uid = get_uid_of_issue("town-has-to-cut-spending")
        search_words = ["swimming pools", "SWIMMING POOLS", "SWIMIng Ploos", "swimming poos"]
        es = self.client
        if not get_availability():
            raise Exception("These are not the results you are looking for")
        else:
            for search_word in search_words:
                search_results = get_suggestions(es, uid, search_word, True)
                for result in search_results:
                    self.assertIn("we should close public <em>swimming</em> <em>pools</em>", result.get("text"))
