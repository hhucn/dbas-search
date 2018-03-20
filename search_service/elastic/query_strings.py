"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
from search_service import FILTER


def settings():
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
                            "tokenizer": "whitespace",
                            "filter": ["synonyms_english"]
                        },
                        "synonyms_german": {
                            "tokenizer": "whitespace",
                            "filter": ["synonyms_german"]
                        }
                    },
                    "filter": {
                        "synonyms_english": {
                            "type": "synonym",
                            "synonyms_path": "synonyms_english.txt"
                        },
                        "synonyms_german": {
                            "type": "synonym",
                            "synonyms_path": "synonyms_german.txt"
                        }
                    }
                }
            }
        }
    }


def search_query(text, uid, position, synonym_analyzer=FILTER.get("en")):
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
    :param position: is the text a start point or not (boolean)
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
                            "isPosition": position
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


def edits_query(text, uid, synonym_analyzer=FILTER.get("en")):
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


def duplicates_or_reasons_query(text, issue_uid, value_uid, synonym_analyzer=FILTER.get("en")):
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


def all_statements_with_value_query(text, uid, synonym_analyzer=FILTER.get("en")):
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


def data_mapping(text, start_point, uid, lang_id, statement_uid):
    """
    The data format used in the database

    :param text: text to be added
    :param start_point: is the text a start point
    :param uid: in which id should the text be added
    :param lang_id: which language is used
    :param statement_uid: to determine the language of the current issue
    :return: data map of the data-format used in the elastic search index
    """
    return (
        {
            "isPosition": start_point,
            "textversions": {
                "content": text,
                "statementUid": statement_uid
            },
            "issues": {
                "uid": uid,
                "langUid": lang_id
            }
        }
    )
