import requests

from search_service.database_handling.query_with_graphql import graphql_query, query_all_data_by_uid, \
    pretty_print
from search_service.elastic.elastic_search import create_elastic_search_client, index_query_result_text_versions, \
    shape_search_string, search_in_statements_with_query, setting_string, \
    query_string_synonym_text_search


def get_all_matching_statements_by_uid_and_synonyms(es, uid, search, is_startpoint):
    """
    Searches for a word in field content.
    "*" means start with or end with.
    Therefore ("*" + text + "*") search for text in content.

    :param uid: is the uid of the current discussion
    :param search: is the search word
    :param is_startpoint: filters the content for startpoints
    :return: all results of the elastic search of a given search word with highlighting
    """

    index_name = "post_statements"
    if es.ping() is False:
        raise Exception("Elastic is not available")
    else:
        result_list = []

        content = graphql_query(query_all_data_by_uid(uid, is_startpoint))

        if not content:
            return result_list

        settings = setting_string()

        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name,
                              body=settings)
        else:
            requests.put("http://elasticsearch:9200/"+index_name, data=settings)

        index_query_result_text_versions(es, content.get("statements"))

        search = shape_search_string(search)

        query = query_string_synonym_text_search(search)

        search_results = search_in_statements_with_query(es, query)

        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)

        for result in search_results.get("hits").get("hits"):
            result_list.append(result.get("highlight").get("content")[0])

        return result_list


def get_strings_for_suggestion(es, uid, search, is_startpoint):
    results = get_all_matching_statements_by_uid_and_synonyms(es, uid, search, is_startpoint)
    content_to_show = []
    for result in results:
        # todo work on second tags
        filling = {"text": "Fits: " + result}
        content_to_show.append(filling)
    return content_to_show


if __name__ == "__main__":
    es = create_elastic_search_client()
    assert (es.ping())
    """
    print(es.indices.exists(index="post_statements"))
    es.indices.delete(index="post_statements")
    print(es.indices.exists(index="post_statements"))
    """
    result = get_strings_for_suggestion(es, 2, "get doggy", True)
    pretty_print(result)

    """

    es = create_elastic_search_client()
    assert (es.ping())

    response = graphql_query(query_all_data_by_uid(4, True))
    response = response.get('statements')

    index_name = "statements24"

    for i in range(1, 25):
        print(es.indices.exists("statements" + str(i)))

    settings = setting_string()

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

    text = "get a cat"
    search_query = query_string_synonym_text_search(text)

    result = es.search(index=index_name, doc_type="json", body=search_query)
    pretty_print(result)
    
    print(es.indices.exists(index="post_statments"))
    """
