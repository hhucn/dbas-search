import unittest

from search_service.database_handling.query_with_graphql import get_uid_of_issue, pretty_print
from search_service.elastic.elastic_search_helper import is_elastic_search_available
from search_service.experimental.experiment_index_verwaltung import create_elastic_search_connection, INDEX_NAME, \
    get_all_matching_statements_by_uid_and_synonyms


class TestAvailability(unittest.TestCase):
    def setUp(self):
        self.client = create_elastic_search_connection()
        self.assertTrue(self.client.ping())
        self.assertTrue(is_elastic_search_available())

    def test_index_exists(self):
        self.assertTrue(self.client.indices.exists(index=INDEX_NAME))


class TestElasticSearchSynonymResults(unittest.TestCase):
    def setUp(self):
        self.client = create_elastic_search_connection()

    def test_synonym_doggy_is_dog(self):
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"))
        else:
            results = get_all_matching_statements_by_uid_and_synonyms(es, 2, "doggy ", True)

            for res in results:
                tmp = res.replace("<em>", "").replace("</em>", "")
                results[results.index(res)] = tmp

            self.assertIsNotNone(results)
            self.assertTrue("we should get a dog" in results)
            self.assertTrue("we could get both, a cat and a dog" in results)

    def test_synonym_kitty_is_cat(self):
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"))
        else:
            results = get_all_matching_statements_by_uid_and_synonyms(es, 2, "cat", True)

            for res in results:
                tmp = res.replace("<em>", "").replace("</em>", "")
                results[results.index(res)] = tmp

            self.assertIsNotNone(results)
            self.assertTrue("we should get a cat" in results)
            self.assertTrue("we could get both, a cat and a dog" in results)

    def test_full_text_search_with_synonyms(self):
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"))
        else:
            results = get_all_matching_statements_by_uid_and_synonyms(es, 2, "get cat", True)

            for res in results:
                tmp = res.replace("<em>", "").replace("</em>", "")
                results[results.index(res)] = tmp

            self.assertIsNotNone(results)
            self.assertTrue("we should get a cat" in results)
            self.assertTrue("we could get both, a cat and a dog" in results)
            self.assertTrue("we should get a dog" in results)

    def test_full_text_search_with_highlighting(self):
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"))
        else:
            # Todo: What is with the blank space behind the last word ?
            results = get_all_matching_statements_by_uid_and_synonyms(es, 2, "we kitty ", True)
            self.assertIsNotNone(results)
            self.assertTrue("<em>we</em> should get a <em>cat</em>" in results)
            self.assertTrue("<em>we</em> could get both, a <em>cat</em> and a dog" in results)
            self.assertTrue("<em>we</em> should get a dog" in results)

    def test_full_text_search_with_highlighting_and_mixed_sentence(self):
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"))
        else:
            results = get_all_matching_statements_by_uid_and_synonyms(es, 2, "the kitty should get a doggy ", True)
            self.assertIsNotNone(results)

            self.assertTrue("we <em>should</em> <em>get</em> <em>a</em> <em>cat</em>" in results)
            self.assertTrue(
                "we could <em>get</em> both, <em>a</em> <em>cat</em> <em>and</em> <em>a</em> <em>dog</em>" in results)
            self.assertTrue("we <em>should</em> <em>get</em> <em>a</em> <em>dog</em>" in results)

    def test_highlighting_is_none_but_there_is_no_exception(self):
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"))
        else:
            try:
                result = get_all_matching_statements_by_uid_and_synonyms(es, 2, "kitty is ", True)
                self.assertIsNotNone(result)
            except AttributeError:
                self.assertTrue(False)

            pass


class TestElasticSearchSearchResultsByUid(unittest.TestCase):
    def setUp(self):
        self.client = create_elastic_search_connection()

    def test_find_auto_in_elektroautos_uid(self):
        uid = get_uid_of_issue("elektroautos")
        search_word = "Auto"
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"),
                              get_all_matching_statements_by_uid_and_synonyms(es, uid, search_word, True))

        else:
            search_results = get_all_matching_statements_by_uid_and_synonyms(es, uid, search_word, True)
            self.assertIsNotNone(search_results)

            for res in search_results:
                tmp = res.replace("<em>", "").replace("</em>", "")
                search_results[search_results.index(res)] = tmp

            self.assertTrue("E-Autos \"optimal\" f\u00fcr den Stadtverkehr sind" in search_results)
            self.assertTrue("E-Autos das autonome Fahren vorantreiben" in search_results)

    def test_find_auto_wrong_writing_in_elektroautos_uid(self):
        uid = get_uid_of_issue("elektroautos")

        search_words = [
            "AUTOS", "AuToS", "aUtOs", "aUt", "autos"
        ]
        es = self.client
        for word in search_words:
            if not is_elastic_search_available():
                self.assertRaises(Exception("Elastic is not available"),
                                  get_all_matching_statements_by_uid_and_synonyms(es, uid, word, True))
            else:
                search_results = get_all_matching_statements_by_uid_and_synonyms(es, uid, word, True)
                pretty_print(search_results)
                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertIsNotNone(search_results)
                self.assertTrue("E-Autos \"optimal\" f\u00fcr den Stadtverkehr sind" in search_results)
                self.assertTrue("E-Autos das autonome Fahren vorantreiben" in search_results)


class TestGermanSynonyms(unittest.TestCase):
    def setUp(self):
        self.client = create_elastic_search_connection()

    def test_highlighting_is_none_but_there_is_no_exception(self):
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"))
        else:
            try:
                result = get_all_matching_statements_by_uid_and_synonyms(es, 4, "selber ", True)
                self.assertIsNotNone(result)
            except AttributeError:
                self.assertTrue(False)

            pass

    def test_german_synonym_is_highlighted(self):
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"))
        else:
            results = get_all_matching_statements_by_uid_and_synonyms(es, 4, "selber ", True)
            self.assertIsNotNone(results)
            self.assertTrue("E-Autos das <em>autonome</em> Fahren vorantreiben" in results)

    def test_german_fuzziness(self):
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"))
        else:
            results = get_all_matching_statements_by_uid_and_synonyms(es, 4, "Fahrten", True)
            self.assertIsNotNone(results)
            self.assertTrue("E-Autos das autonome <em>Fahren</em> vorantreiben" in results)
