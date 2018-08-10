class ESQuery:

    def __init__(self, field: str = "text:", text: str = "", fuzziness: int = 3, synonym_boost: int = 5):
        self.field = field
        self.text = text
        self.synonym_boost = synonym_boost
        self.fuzziness = fuzziness

    def german_infix_search(self):
        """
        This query does a infix search with german synonyms.

        :return: German infix search query for german synonyms.
        """
        return {
            "query": {
                "query_string": {
                    "fields": [self.field],
                    "query": "*" + self.text + "*" if self.text else self.text,
                    "fuzziness": self.fuzziness,
                    "analyzer": "synonyms_german",
                    "analyze_wildcard": False,
                    "auto_generate_synonyms_phrase_query": True
                }
            }
        }

    def english_infix_search(self):
        """
        This query does a infix search with english synonyms.

        :return: German infix search query for english synonyms.
        """
        return {
            "query": {
                "query_string": {
                    "fields": [self.field],
                    "query": "*" + self.text + "*" if self.text else self.text,
                    "fuzziness": self.fuzziness,
                    "analyzer": "synonyms_english",
                    "analyze_wildcard": False,
                    "auto_generate_synonyms_phrase_query": True
                }
            }
        }

    def german_infix_keyword_search(self):
        """
        This query does a infix search with german synonyms.

        :return: German infix search query for german synonyms.
        """
        return {
            "query": {
                "query_string": {
                    "fields": [self.field],
                    "query": "*" + self.text + "*" if self.text else self.text,
                    "fuzziness": self.fuzziness,
                    "analyzer": "keyword_synonyms_german",
                    "analyze_wildcard": False,
                    "auto_generate_synonyms_phrase_query": True
                }
            }
        }

    def english_infix_keyword_search(self):
        """
        This query does a infix search with english synonyms.

        :return: German infix search query for english synonyms.
        """
        return {
            "query": {
                "query_string": {
                    "fields": [self.field],
                    "query": "*" + self.text + "*" if self.text else self.text,
                    "fuzziness": self.fuzziness,
                    "analyzer": "keyword_synonyms_english",
                    "analyze_wildcard": False,
                    "auto_generate_synonyms_phrase_query": True
                }
            }
        }

    def english_synonym_search(self):
        """
        This query boosts english synonyms.

        :return: Boost query for english synonyms.
        """
        return {
            "query": {
                "match_phrase": {
                    "text": {
                        "query": self.text,
                        "analyzer": "synonyms_english",
                        "boost": self.synonym_boost
                    }
                }
            }
        }

    def german_synonym_search(self):
        """
        This query boosts german synonyms.

        :return: Boost query for german synonyms.
        """
        return {
            "query": {
                "match_phrase": {
                    "text": {
                        "query": self.text,
                        "analyzer": "synonyms_german",
                        "boost": self.synonym_boost
                    }
                }
            }
        }

    def simple_match_phrase(self, analyzer: str = "synonyms_german"):
        """
        This is a simple query for a match_phrase with a specific analyzer.

        :param analyzer: The analyzer to be used while searching
        :return:
        """
        return {
            "query": {
                "match_phrase": {
                    "text": {
                        "query": self.text,
                        "analyzer": analyzer
                    }
                }
            }
        }

    def simple_query_string(self, analyzer: str = "synonyms_german"):
        """
        This is a simple query for a query_string with wildcards, and a specific analyzer.

        :param analyzer: The analyzer to be used while searching
        :return:
        """
        return {
            "query": {
                "query_string": {
                    "analyzer": analyzer,
                    "query": "*" + self.text + "*",
                    "fields": [self.field],
                }
            }
        }

    def simple_fuzzy_search(self):
        """
        This is a simple query for fuzzy search.

        :return:
        """
        return {
            "query": {
                "match": {
                    "text": {
                        "query": self.text,
                        "fuzziness": "AUTO",
                        "prefix_length": 1
                    }
                }
            }
        }

    def semantic_search_query(self):
        """
        This query combines all queries necessary for a semantic search.

        :return: Semantic search query.
        """
        return {
            "query": {
                "bool": {
                    "should": [
                        self.simple_match_phrase(analyzer="synonyms_english").get("query"),
                        self.simple_match_phrase(analyzer="synonyms_german").get("query"),
                        self.simple_query_string(analyzer="synonyms_english").get("query"),
                        self.simple_query_string(analyzer="synonyms_german").get("query"),
                        self.simple_fuzzy_search().get("query")
                    ]
                }
            }
        }
