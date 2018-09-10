"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
from core import FILTER


def settings() -> dict:
    """
    The setting string for the client.
    Notice: the synonym files are stored in config/.

    :return: settings of the elastic search index
    """
    return {
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "synonyms_english": {
                            "expand": True,
                            "tokenizer": "whitespace",
                            "filter": ["lowercase", "synonyms_english"]
                        },
                        "synonyms_german": {
                            "expand": True,
                            "tokenizer": "whitespace",
                            "filter": ["lowercase", "synonyms_german"]
                        },
                        "keyword_synonyms_english": {
                            "expand": True,
                            "tokenizer": "keyword",
                            "filter": ["lowercase", "synonyms_english"]
                        },
                        "keyword_synonyms_german": {
                            "expand": True,
                            "tokenizer": "keyword",
                            "filter": ["lowercase", "synonyms_german"]
                        }
                    },
                    "filter": {
                        "synonyms_english": {
                            "expand": True,
                            "type": "synonym",
                            "synonyms_path": "synonyms_english.txt"
                        },
                        "synonyms_german": {
                            "expand": True,
                            "type": "synonym",
                            "synonyms_path": "synonyms_german.txt"
                        }
                    }
                }
            }
        }
    }


def search_query(text: str, uid: int, is_position: bool, synonym_analyzer: str = FILTER.get("en")) -> dict:
    """
    The search query uses synonyms and fuzzy search in regard to a full text search.
    Notice that there are three parts.
        (1) The synonym part to work with synonyms. They are stored in config.
        (2) The text search part to find a word or substring in a text.
            (* is to ignore previous or following words etc.)
        (3) Fuzzi part to add a fuzziness the the search

    force_source forces the output to highlight by every of the three parts mentioned above.

    :param text: the text to be searched (text)
    :param uid: uid of the issue to be looked up
    :param is_position: is the text a start point or not (boolean)
    :param synonym_analyzer: the analyzer to be used for the synonyms (english or german)
    :return: search query for searching specific elements filtered by uid, and start_point
    """
    return {
        "query": {
            "bool": {

                "should": [
                    {
                        "match_phrase": {
                            "textversions.content": {
                                "query": text,
                                "analyzer": synonym_analyzer
                            }
                        }
                    },
                    {
                        "query_string": {
                            "analyzer": synonym_analyzer,
                            "query": "*" + text + "*",
                            "fields": ["textversions.content"],
                        }
                    },
                    {
                        "match": {
                            "textversions.content": {
                                "query": text,
                                "fuzziness": "AUTO",
                                "prefix_length": 1
                            }
                        }
                    }
                ],
                "must": [
                    {
                        "match": {
                            "issues.uid": uid
                        }
                    },
                    {
                        "match": {
                            "isPosition": is_position
                        }
                    }
                ]
            }
        },
        '_source': ['textversions.content', 'textversions.statementUid'],
        'highlight': {
            "pre_tags": ["<em>"],
            "post_tags": ["</em>"],
            'fields': {
                'textversions.content': {
                    "force_source": "true",
                    "highlight_query": {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "textversions.content": {
                                            "query": text,
                                            "analyzer": synonym_analyzer
                                        }
                                    }
                                },
                                {
                                    "query_string": {
                                        "analyzer": synonym_analyzer,
                                        "query": "*" + text + "*",
                                        "fields": ["textversions.content"],
                                    }
                                },
                                {
                                    "match": {
                                        "textversions.content": {
                                            "query": text,
                                            "fuzziness": "AUTO",
                                            "prefix_length": 1
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
    }


def edits_query(text: str, uid: int, synonym_analyzer: str = FILTER.get("en")) -> dict:
    """
    This query works like the search_query.

    :param text: the text to be searched
    :param uid: uid of the issue to be looked up
    :param synonym_analyzer: the analyzer to be used for the synonyms (english or german)
    :return: search query for edits filtered by the issue.uid
    """
    return {
        "query": {
            "bool": {

                "should": [
                    {
                        "match_phrase": {
                            "textversions.content": {
                                "query": text,
                                "analyzer": synonym_analyzer
                            }
                        }
                    },
                    {
                        "query_string": {
                            "analyzer": synonym_analyzer,
                            "query": "*" + text + "*",
                            "fields": ["textversions.content"],
                        }
                    },
                    {
                        "match": {
                            "textversions.content": {
                                "query": text,
                                "fuzziness": "AUTO",
                                "prefix_length": 1
                            }
                        }
                    }
                ],
                "must": [
                    {
                        "match": {
                            "textversions.statementUid": uid
                        }
                    }
                ]
            }
        },
        '_source': ['textversions.content', 'textversions.statementUid'],
        'highlight': {
            "pre_tags": ["<em>"],
            "post_tags": ["</em>"],
            'fields': {
                'textversions.content': {
                    "force_source": "true",
                    "highlight_query": {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "textversions.content": {
                                            "query": text,
                                            "analyzer": synonym_analyzer
                                        }
                                    }
                                },
                                {
                                    "query_string": {
                                        "analyzer": synonym_analyzer,
                                        "query": "*" + text + "*",
                                        "fields": ["textversions.content"],
                                    }
                                },
                                {
                                    "match": {
                                        "textversions.content": {
                                            "query": text,
                                            "fuzziness": "AUTO",
                                            "prefix_length": 1
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
    }


def duplicates_or_reasons_query(text: str, issue_uid: int, value_uid: int,
                                synonym_analyzer: str = FILTER.get("en")) -> dict:
    """
    This query works like search_query.

    :param text: text to be searched for
    :param issue_uid: uid of the issue to be looked up
    :param value_uid: uid of the statement which is a duplicate or a reason
    :param synonym_analyzer: the analyzer to be used for the synonyms (english or german)
    :return: search query for duplicates or reasons filtered by the issue.uid and a statement.uid
    """
    return {
        "query": {
            "bool": {
                "should": [
                    {
                        "match_phrase": {
                            "textversions.content": {
                                "query": text,
                                "analyzer": synonym_analyzer
                            }
                        }
                    },
                    {
                        "query_string": {
                            "analyzer": synonym_analyzer,
                            "query": "*" + text + "*",
                            "fields": ["textversions.content"],
                        }
                    },
                    {
                        "match": {
                            "textversions.content": {
                                "query": text,
                                "fuzziness": "AUTO",
                                "prefix_length": 1
                            }
                        }
                    }
                ],
                "must": [
                    {
                        "match": {
                            "issues.uid": issue_uid
                        }
                    }
                ],
                "must_not": [
                    {
                        "match": {
                            "textversions.statementUid": value_uid
                        }
                    }
                ]
            }
        },
        '_source': ['textversions.content', 'textversions.statementUid'],
        'highlight': {
            "pre_tags": ["<em>"],
            "post_tags": ["</em>"],
            'fields': {
                'textversions.content': {
                    "force_source": "true",
                    "highlight_query": {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "textversions.content": {
                                            "query": text,
                                            "analyzer": synonym_analyzer
                                        }
                                    }
                                },
                                {
                                    "query_string": {
                                        "analyzer": synonym_analyzer,
                                        "query": "*" + text + "*",
                                        "fields": ["textversions.content"],
                                    }
                                },
                                {
                                    "match": {
                                        "textversions.content": {
                                            "query": text,
                                            "fuzziness": "AUTO",
                                            "prefix_length": 1
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
    }


def all_statements_with_value_query(text: str, uid: int, synonym_analyzer: str = FILTER.get("en")) -> dict:
    """
    This query works like search_query.

    :param text: text to be searched
    :param uid: uid of the issue to be looked up
    :param synonym_analyzer: the analyzer to be used for the synonyms (english or german)
    :return: a search query for statements to a given value filtered by a issue.uid
    """
    return {
        "query": {
            "bool": {
                "should": [
                    {
                        "match_phrase": {
                            "textversions.content": {
                                "query": text,
                                "analyzer": synonym_analyzer
                            }
                        }
                    },
                    {
                        "query_string": {
                            "analyzer": synonym_analyzer,
                            "query": "*" + text + "*",
                            "fields": ["textversions.content"],
                        }
                    },
                    {
                        "match": {
                            "textversions.content": {
                                "query": text,
                                "fuzziness": "AUTO",
                                "prefix_length": 1
                            }
                        }
                    }
                ],
                "must": [
                    {
                        "match": {
                            "issues.uid": uid
                        }
                    }
                ]
            }
        },
        '_source': ['textversions.content', 'textversions.statementUid'],
        'highlight': {
            "pre_tags": ["<em>"],
            "post_tags": ["</em>"],
            'fields': {
                'textversions.content': {
                    "force_source": "true",
                    "highlight_query": {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "textversions.content": {
                                            "query": text,
                                            "analyzer": synonym_analyzer
                                        }
                                    }
                                },
                                {
                                    "query_string": {
                                        "analyzer": synonym_analyzer,
                                        "query": "*" + text + "*",
                                        "fields": ["textversions.content"],
                                    }
                                },
                                {
                                    "match": {
                                        "textversions.content": {
                                            "query": text,
                                            "fuzziness": "AUTO",
                                            "prefix_length": 1
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
    }


def data_mapping(text: str, is_position: bool, uid: int, language: str, statement_uid: int) -> dict:
    """
    The data format used in the database

    :param text: text to be added
    :param is_position: is the text a start point
    :param uid: in which id should the text be added
    :param language: which language is used
    :param statement_uid: to determine the language of the current issue
    :return: data map of the data-format used in the elastic search index
    """
    return (
        {
            "isPosition": is_position,
            "textversions": {
                "content": text,
                "statementUid": statement_uid
            },
            "issues": {
                "uid": uid,
                "langUid": language
            }
        }
    )


def update_textversion(element: dict) -> dict:
    """
    Query to update a textversion and all regarding information by its statement uid.

    :param element: must match the data mapping
    :return:
    """
    isPosition = element.get("isPosition")
    text = element.get("textversions").get("content")
    statementUid = element.get("textversions").get("statementUid")
    issueUid = element.get("issues").get("uid")
    issueLang = element.get("issues").get("langUid")

    return {
        "query": {
            "match": {
                "textversions.statementUid": statementUid
            }
        },
        "script": {
            "inline": "ctx._source.isPosition={0};"
                      "ctx._source.textversions.content='{1}';"
                      "ctx._source.textversions.statementUid={2};"
                      "ctx._source.issues.uid={3};"
                      "ctx._source.issues.langUid='{4}';".format(str(isPosition).lower(), text, statementUid, issueUid,
                                                                 issueLang),
            "lang": "painless"
        }
    }


def update_issue(element: dict) -> dict:
    """
    Query to update a issue by its issue uid.

    :param element: Must match the data mapping
    :return:
    """
    uid = element.get("issues").get("uid")
    language = element.get("issues").get("langUid")

    return {
        "query": {
            "match": {
                "issues.uid": uid
            }
        },
        "script": {
            "inline": "ctx._source.issues.uid='{0}';"
                      "ctx._source.issues.langUid='{1}';".format(uid, language),
            "lang": "painless"
        }
    }


def update_statement(element: dict) -> dict:
    """
    Query to update a statement by its statement uid.

    :param element: must match data mapping
    :return:
    """
    statementUid = element.get("textversions").get("statementUid")
    isPosition = element.get("isPosition")

    return {
        "query": {
            "match": {
                "textversions.statementUid": statementUid
            }
        },
        "script": {
            "inline": "ctx._source.isPosition={0};".format(str(isPosition).lower()),
            "language": "painless"
        }
    }
