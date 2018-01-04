from elasticsearch import Elasticsearch

from search_service import ELASTIC_SEARCH_PORT, ELASTIC_SEARCH_ADDRESS, FILTER


def is_elastic_search_available():
    es = Elasticsearch([{"host": ELASTIC_SEARCH_ADDRESS, "port": ELASTIC_SEARCH_PORT}])
    return es.ping()


def setting_string():
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


def query_search(text, uid, startpoint, synonym_analyzer=FILTER.get("en")):
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
                                "fuzziness": 2,
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
                            "isStartpoint": startpoint
                        }
                    }
                ]
            }
        },
        '_source': ['textversions.content'],
        'highlight': {
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
                                            "fuzziness": 2,
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


def query_string_by_whitespace(text):
    """

    Searches for a word in field content.
    "*" means start with or end with.
    Therefore ("*" + text + "*") search for text in content.

    :param text: search word
    :return: query for the string
    """

    return {
        "query": {
            "query_string": {
                "analyzer": "whitespace",
                "query": "*" + text + "*",
                "fields": ["content"],
            }
        },
        "_source": ["content"],
        "highlight": {
            "fields": {
                "content": {}
            }
        }
    }


def query_string_synonyms_search(text):
    return {
        "query": {
            "match_phrase": {
                "content": {
                    "query": text,
                    "analyzer": "synonyms_english"
                }
            }
        },
        '_source': ['content'],
        'highlight': {
            'fields': {
                'content': {}
            }
        }
    }


def query_string_synonym_text_search(text, synonym_analyzer="synonyms_english"):
    # change analyzer in query_string to the same in match_phrase
    # whitespace or my_synonyms
    return {

        "query": {
            "bool": {
                "should": [
                    {
                        "match_phrase": {
                            "content": {
                                "query": text,
                                "analyzer": synonym_analyzer
                            }
                        }
                    },

                    {
                        "query_string": {
                            "analyzer": synonym_analyzer,
                            "query": "*" + text + "*",
                            "fields": ["content"],
                        }
                    },
                    {
                        "match": {
                            "content": {
                                "query": text,
                                "fuzziness": 2,
                                "prefix_length": 1
                            }
                        }
                    }
                ]
            }
        },

        "highlight": {
            "number_of_fragments": 0,
            "require_field_match": "false",
            "fields": {
                "content": {
                    "force_source": "true",
                    "highlight_query": {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "content": {
                                            "query": text,
                                            "analyzer": synonym_analyzer
                                        }
                                    }
                                },

                                {
                                    "query_string": {
                                        "analyzer": synonym_analyzer,
                                        "query": "*" + text + "*",
                                        "fields": ["content"],
                                    }
                                },
                                {
                                    "match": {
                                        "content": {
                                            "query": text,
                                            "fuzziness": 2,
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


def query_exact_term(term, where):
    return {
        "query": {
            "match_phrase": {
                where: term
            }
        }
    }


def data_mapping(text, is_startpoint, uid, langUid):
    return (
        {
            "isStartpoint": is_startpoint,
            "textversions": {
                "content": text
            },
            "issues": {
                "uid": uid,
                "langUid": langUid
            }
        }
    )
