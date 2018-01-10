"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
from search_service import FILTER


def settings():
    """
    The setting string for the client.
    Notice: the synonym files are stored in config/.

    :return:
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


def search_query(text, uid, start_point, synonym_analyzer=FILTER.get("en")):
    """
    The search query uses synonyms and fuzzy search in regard to a full text search.
    Notice that there are three parts.
        (1) The synonym part to work with synonyms. They are stored in config.
        (2) The text search part to find a word or substring in a text.
            (* is to ignore previous or following words etc.)
        (3) Fuzzi part to add a fuzziness the the search

    force_source forces the output to highlight by every of the three parts mentioned above.

    :param text: the text to be searched (text)
    :param uid: the uid of the current issue (int)
    :param start_point: is the text a start point or not (boolean)
    :param synonym_analyzer: the analyzer to be used for the synonyms (english or german)
    :return:
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
                            "isStartpoint": start_point
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


def query_exact_term(term, where):
    """
    Query exact terms.

    :param term: to be searched
    :param where: which field (e.g. "textversions.content")
    :return:
    """
    return {
        "query": {
            "match_phrase": {
                where: term
            }
        }
    }


def data_mapping(text, start_point, uid, lang_id):
    """
    The data format used in the database

    :param text: text to be added
    :param start_point: is the text a start point
    :param uid: in which id should the text be added
    :param lang_id: which language is used
    :return:
    """
    return (
        {
            "isStartpoint": start_point,
            "textversions": {
                "content": text
            },
            "issues": {
                "uid": uid,
                "langUid": lang_id
            }
        }
    )
