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
                    "analyze_wildcard": True,
                    "auto_generate_synonyms_phrase_query": False
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
                    "analyze_wildcard": True,
                    "auto_generate_synonyms_phrase_query": False
                }
            }
        }

    def german_infix_keyword_search(self, ):
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

    def semantic_search_query(self):
        """
        This query combines all queries necessary for a semantic search.

        :return: Semantic search query.
        """
        return {
            "query": {
                "bool": {
                    "should": [
                        self.german_synonym_search().get("query"),
                        self.english_synonym_search().get("query"),
                        self.german_infix_keyword_search().get("query"),
                        self.english_infix_keyword_search().get("query"),
                        self.german_infix_search().get("query"),
                        self.english_infix_search().get("query")
                    ]
                }
            }
        }
