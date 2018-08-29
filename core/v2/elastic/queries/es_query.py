from core.v2.sql.db_models.author import Author
from core.v2.sql.db_models.issue import Issue
from core.v2.sql.db_models.statement import Statement


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

    @staticmethod
    def update_textversion_information(statement_uid: int, element: dict) -> dict:
        """
        Update all information of a specific statement.

        :param statement_uid: The uid of the statement that should be updated
        :param element: The element that contains all the necessary information for the update.
                        Must fit the Author, Issue, Statement
        :return:
        """
        author = Author(element)
        issue = Issue(element)
        statement = Statement(element)
        return {
            "query": {
                "match": {
                    "uid": statement_uid
                }
            },
            "script": {
                "inline": "ctx._source.author.nickname='{0}';"
                          "ctx._source.author.uid={1};"
                          "ctx._source.isPosition={2};"
                          "ctx._source.issue.info='{3}';"
                          "ctx._source.issue.lang='{4}';"
                          "ctx._source.issue.slug='{5}';"
                          "ctx._source.issue.title='{6}';"
                          "ctx._source.issue.uid={7};"
                          "ctx._source.text='{8}';"
                          "ctx._source.uid={9}".format(author.nickname, author.uid, str(statement.isPosition).lower(),
                                                       issue.info,
                                                       issue.lang, issue.slug, issue.title, issue.uid,
                                                       statement.text, statement_uid),
                "lang": "painless"
            }
        }

    @staticmethod
    def update_issue_information(issue_uid: int, element: dict) -> dict:
        """
        Update the issue information of a specific document.

        :param issue_uid: The issue uid of the document that gets an update
        :param element: The element that contains all necessary information for the update.
                        Must fit Issue.
        :return:
        """
        issue = Issue(element)
        print(issue.__json__())
        return {
            "query": {
                "match": {
                    "issue.uid": issue_uid
                }
            },
            "script": {
                "inline": "ctx._source.issue.info='{0}';"
                          "ctx._source.issue.lang='{1}';"
                          "ctx._source.issue.slug='{2}';"
                          "ctx._source.issue.title='{3}';"
                          "ctx._source.issue.uid={4};".format(issue.info, issue.lang, issue.slug, issue.title,
                                                              issue.uid),
                "lang": "painless"
            }
        }

    @staticmethod
    def update_author_information(author_uid: int, element: dict) -> dict:
        """
        Update the author information of a specific document.

        :param author_uid: The uid of the author that is updated.
        :param element: The element that contains all information about the updated author.
                        Must fit author.
        :return:
        """
        author = Author(element)
        print(author.__json__())
        return {
            "query": {
                "match": {
                    "author.uid": author_uid
                }
            },
            "script": {
                "inline": "ctx._source.author.nickname='{0}';"
                          "ctx._source.author.uid={1};".format(author.nickname, author.uid),
                "lang": "painless"
            }
        }

    @staticmethod
    def update_statement_information(statement_uid: int, is_position: bool) -> dict:
        """
        Update a statement position.

        :param is_position: The value of the statement if it is a position or not.
        :param statement_uid: The uid of the statement that should be updated.
        :return:
        """
        return {
            "query": {
                "match": {
                    "uid": statement_uid
                }
            },
            "script": {
                "inline": "ctx._source.isPosition={0};".format(str(is_position).lower()),
                "lang": "painless"
            }
        }
