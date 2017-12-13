from search_service.database_handling.query_with_graphql import graphql_query, query_all_data_by_uid, \
    pretty_print
import requests
from search_service.elastic.elastic_search import create_elastic_search_client

if __name__ == "__main__":

    es = create_elastic_search_client()
    assert (es.ping())

    response = graphql_query(query_all_data_by_uid(2, True))
    response = response.get('statements')

    index_name = "statements24"

    settings = {
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "my_synonyms": {
                            "tokenizer": "whitespace",
                            "filter": ["my_synonyms"]
                        }
                    },
                    "filter": {
                        "my_synonyms": {
                            "type": "synonym",
                            "synonyms_path": "synonyms.txt"
                        }
                    }
                }
            }
        }
    }

    if not es.indices.exists(index_name):
        es.indices.create(
            index=index_name,
            body=settings
        )
    else:
        requests.put("http://elasticsearch:9200/" + index_name, data=settings)

    for i in range(0, len(response)):
        content = {
            "content": response[i].get("textversions").get("content")
        }

        es.index(index=index_name, doc_type="json", id=i, body=content)

    text = "doggy"
    search_query = {
        "query": {
            "match_phrase": {
                "content": {
                    "query": text,
                    "analyzer": "my_synonyms"
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

    result = es.search(index=index_name, doc_type="json", body=search_query)
    pretty_print(result)
