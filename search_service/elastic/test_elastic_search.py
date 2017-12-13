import unittest

from search_service.database_handling.query_with_graphql import query_all_users_nicknames_with_issues, \
    get_uid_of_issue
from search_service.elastic.elastic_search import graphql_query, create_elastic_search_connection, \
    get_all_matching_statements_by_uid, get_all_matching_statements_by_uid_and_synonyms
from search_service.elastic.elastic_search_helper import is_elastic_search_available


class TestElasticsearch(unittest.TestCase):
    def setUp(self):
        self.client = create_elastic_search_connection()

    def test_elastic_search_is_available(self):
        self.assertTrue(is_elastic_search_available())

    def test_query_results_not_none(self):
        result = graphql_query(query_all_users_nicknames_with_issues())
        self.assertIsNotNone(result)

    def test_elastic_search_is_created_correctly(self):
        self.assertTrue(self.client.ping())


class TestElasticSearchSearchResultsByUid(unittest.TestCase):
    def setUp(self):
        self.client = create_elastic_search_connection()

    def test_find_auto_in_elektroautos_uid(self):
        uid = get_uid_of_issue("elektroautos")
        search_word = "Auto"
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"),
                              get_all_matching_statements_by_uid(es, uid, search_word, True))

        else:
            search_results = get_all_matching_statements_by_uid(es, uid, search_word, True)
            self.assertIsNotNone(search_results)

            for res in search_results:
                tmp = res.replace("<em>", "").replace("</em>", "")
                search_results[search_results.index(res)] = tmp

            self.assertTrue("E-Autos \"optimal\" f\u00fcr den Stadtverkehr sind" in search_results)
            self.assertTrue("E-Autos das autonome Fahren vorantreiben" in search_results)

    def test_find_auto_wrong_writing_in_elektroautos_uid(self):
        uid = get_uid_of_issue("elektroautos")

        search_words = [
            "AUTOS", "AuToS", "aUtOs", "a", "A", "au", "AU", "aUt", "autos"
        ]
        es = self.client
        for word in search_words:
            if not is_elastic_search_available():
                self.assertRaises(Exception("Elastic is not available"),
                                  get_all_matching_statements_by_uid(es, uid, word, True))
            else:
                search_results = get_all_matching_statements_by_uid(es, uid, word, True)

                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertIsNotNone(search_results)
                self.assertTrue("E-Autos \"optimal\" f\u00fcr den Stadtverkehr sind" in search_results)
                self.assertTrue("E-Autos das autonome Fahren vorantreiben" in search_results)

    def test_find_e_autos_in_elektroautos_uid(self):

        uid = get_uid_of_issue("elektroautos")
        search_words = [
            "E", "E-A", "E-Au", "E-Aut", "E-Auto", "E-Autos"
        ]
        es = self.client
        for word in search_words:
            if not is_elastic_search_available():
                self.assertRaises(Exception("Elastic is not available"),
                                  get_all_matching_statements_by_uid(es, uid, word, True))
            else:
                search_results = get_all_matching_statements_by_uid(es, uid, word, True)

                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertIsNotNone(search_results)
                self.assertTrue("E-Autos \"optimal\" f\u00fcr den Stadtverkehr sind" in search_results)
                self.assertTrue("E-Autos das autonome Fahren vorantreiben" in search_results)

    def test_find_e_autos_wrong_writing_in_elektroautos_uid(self):
        uid = get_uid_of_issue("elektroautos")
        search_words = [
            "e", "e-A", "-AU", "E+AuTo", "E Auto", "e autos", "e-autos", "e aut", "E A U T O S"
        ]
        es = self.client
        for word in search_words:
            if not is_elastic_search_available():
                self.assertRaises(Exception("Elastic is not available"),
                                  get_all_matching_statements_by_uid(es, uid, word, True))
            else:
                search_results = get_all_matching_statements_by_uid(es, uid, word, True)

                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertIsNotNone(search_results)
                self.assertTrue("E-Autos \"optimal\" f\u00fcr den Stadtverkehr sind" in search_results)
                self.assertTrue("E-Autos das autonome Fahren vorantreiben" in search_results)

    def test_find_stadtverkehr_in_elektroautos_uid(self):
        uid = get_uid_of_issue("elektroautos")
        search_words = [
            "s", "st", "stad", "stadt", "stadtv", "stadtve", "stadtver", "stadtverk", "stadtverke", "stadtverkeh",
            "stadtverkehr",

            "S", "ST", "STAD", "STADT", "STADTV", "STADTVE", "STADTVER", "STADTVERK", "STADTVERKE", "STADTVERKEH",
            "STADTVERKEHR",

            "TV", "Tv", "DTV", "AD"
        ]
        es = self.client
        for word in search_words:
            if not is_elastic_search_available():
                self.assertRaises(Exception("Elastic is not available"),
                                  get_all_matching_statements_by_uid(es, uid, word, True))
            else:
                search_results = get_all_matching_statements_by_uid(es, uid, word, True)

                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertIsNotNone(search_results)
                self.assertTrue("E-Autos \"optimal\" f\u00fcr den Stadtverkehr sind" in search_results)

    def test_find_special_characters_in_elektroautos_uid(self):
        uid = get_uid_of_issue("elektroautos")
        search_words = ["\u00fc", "ü", "Ü"]
        es = self.client
        for word in search_words:
            if not is_elastic_search_available():
                self.assertRaises(Exception("Elastic is not available"),
                                  get_all_matching_statements_by_uid(es, uid, word, True))
            else:
                search_results = get_all_matching_statements_by_uid(es, uid, word, True)

                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertIsNotNone(search_results)
                self.assertTrue("E-Autos \"optimal\" f\u00fcr den Stadtverkehr sind" in search_results)

    def test_find_tesla_in_elektroautos_uid(self):
        uid = get_uid_of_issue("elektroautos")
        search_words = [
            "Tesla", "tesla"
        ]
        es = self.client
        for word in search_words:
            if not is_elastic_search_available():
                self.assertRaises(Exception("Elastic is not available"),
                                  get_all_matching_statements_by_uid(es, uid, word, False))
            else:
                search_results = get_all_matching_statements_by_uid(es, uid, word, False)

                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertIsNotNone(search_results)
                self.assertTrue(
                    "Tesla mutig bestehende Techniken einsetzt und zeigt was sie k\u00f6nnen" in search_results)

    def test_sentence_with_no_sense_containng_tesla_uid(self):
        uid = get_uid_of_issue("elektroautos")
        search_words = ["asdasd Tesla dasdasd"]
        es = self.client
        for word in search_words:
            if not is_elastic_search_available():
                self.assertRaises(Exception("Elastic is not available"),
                                  get_all_matching_statements_by_uid(es, uid, word, False))
            else:
                search_results = get_all_matching_statements_by_uid(es, uid, word, False)

                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertIsNotNone(search_results)
                self.assertTrue(
                    "Tesla mutig bestehende Techniken einsetzt und zeigt was sie k\u00f6nnen" in search_results)

    def test_sentence_with_sence(self):
        uid = get_uid_of_issue("elektroautos")
        search_words = ["in der Stadt"]
        es = self.client

        for word in search_words:
            if not is_elastic_search_available():
                self.assertRaises(Exception("Elastic is not available"),
                                  get_all_matching_statements_by_uid(es, uid, word, False))
            else:
                search_results = get_all_matching_statements_by_uid(es, uid, word, False)

                for res in search_results:
                    tmp = res.replace("<em>", "").replace("</em>", "")
                    search_results[search_results.index(res)] = tmp

                self.assertIsNotNone(search_results)
                self.assertTrue("die Anzahl an Ladestationen in der Stadt nicht ausreichend ist" in search_results)
                self.assertTrue("dadurch die L\u00e4rmbel\u00e4stigung in der Stadt sinkt" in search_results)
                self.assertTrue(
                    "L\u00e4rmbel\u00e4stigung kein wirkliches Problem in den St\u00e4dten ist" in search_results)


class TestElasticSearchSynonymResults(unittest.TestCase):
    def setUp(self):
        self.client = create_elastic_search_connection()

    def test_synonym_doggy_is_dog(self):
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"))
        else:
            results = get_all_matching_statements_by_uid_and_synonyms(es, 2, "doggy", True)

            for res in results:
                tmp = res.replace("<em>", "").replace("</em>", "")
                results[results.index(res)] = tmp

            self.assertIsNotNone(results)
            self.assertTrue("we could get both, a cat and a dog" in results)
            self.assertTrue("we should get a dog" in results)

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

            self.assertTrue("we <em>should</em> <em>get</em> <em>a</em> <em>dog</em>" in results)
            self.assertTrue(
                "we could <em>get</em> both, <em>a</em> <em>cat</em> <em>and</em> <em>a</em> <em>dog</em>" in results)
            self.assertTrue("we <em>should</em> <em>get</em> <em>a</em> <em>cat</em>" in results)

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
            result = get_all_matching_statements_by_uid_and_synonyms(es, 4, "selber ", True)
            self.assertIsNotNone(result)
            self.assertTrue("E-Autos das <em>autonome</em> Fahren vorantreiben" in result)

    def test_german_fuzziness(self):
        es = self.client
        if not is_elastic_search_available():
            self.assertRaises(Exception("Elastic is not available"))
        else:
            result = get_all_matching_statements_by_uid_and_synonyms(es, 4, "Fahrten", True)
            self.assertIsNotNone(result)
            self.assertTrue("E-Autos das autonome <em>Fahren</em> vorantreiben" in result)
