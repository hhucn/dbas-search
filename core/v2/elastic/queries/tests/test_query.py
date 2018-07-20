import unittest

from core.v2.elastic.queries.es_query import ESQuery


class TestQuery(unittest.TestCase):
    def test_if_all_field_are_set(self):
        query = ESQuery(field="text:", text="Coconut", fuzziness=2).sem_query()
        query = query.get("query").get("query_string")
        self.assertEqual(query.get("fields")[0], "text:")
        self.assertEqual(query.get("query"), "*Coconut*")
        self.assertEqual(query.get("fuzziness"), 2)

    def test_if_query_is_empty_if_text_is_empty(self):
        query = ESQuery().sem_query()
        query = query.get("query").get("query_string")
        self.assertEqual(query.get("query"), "")
