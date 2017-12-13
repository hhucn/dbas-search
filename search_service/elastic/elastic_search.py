from elasticsearch import Elasticsearch

from search_service import FILTER
from search_service.database_handling.query_with_graphql import graphql_query, query_all_data_by_uid, \
    query_every_datas_from_active_issue, query_language_of_issue_by_uid, query_all_uids
from search_service.elastic.elastic_search_helper import setting_string, query_string_by_whitespace, \
    query_string_synonym_text_search, query_search
from search_service import ELASTIC_SEARCH_ADDRESS, ELASTIC_SEARCH_PORT

#ELASTIC_SEARCH_PORT = 9200
#ELASTIC_SEARCH_ADDRESS = "elasticsearch"
INDEX_NAME = "test_index"


def create_elastic_search_client():
    """

    :return: new instance of the elastic client
    """

    return Elasticsearch([{"host": ELASTIC_SEARCH_ADDRESS, "port": ELASTIC_SEARCH_PORT}])


def index_query_result_text_versions(es, content):
    """
    creates one index for every textversion in the result of the graphql response in the elastic client

    :param es: existing instance of the elastic client
    :param content: the result from the graphql request (use content.get("statements"))
    """

    for i in range(len(content)):
        es.index(index="post_statements",
                 doc_type="json",
                 id=i,
                 body=content[i].get("textversions"))
    es.indices.refresh(index="post_statements")


def search_in_statements_with_query(es, query):
    """

    :param es: elastic client
    :param query: query string for the search
    :return results for the elastic search for a string in all of the statements
    """

    return es.search(index="post_statements", doc_type="json", body=query)


def shape_search_string(text):
    """

    Replaces all special characters, because the tokenizer of the index
    splits words like "E-Autos" into [E, Autos].
    Therefore if the search word is E-Autos, the search would have no result.
    By replacing the special characters the search will lead to a success.

    :param text: search word
    :return: filtered search word
    """

    text = text.lower()
    for c in ["+", "-", ".", ":", ","]:
        if c in text:
            text = text.replace(c, " ")

    return text


def get_all_matching_statements_by_uid(es, uid, search, is_startpoint):
    """
    Searches for a word in field content.
    "*" means start with or end with.
    Therefore ("*" + text + "*") search for text in content.

    :param uid: is the uid of the current discussion
    :param search: is the search word
    :param is_startpoint: filters the content for startpoints
    :return: all results of the elastic search of a given search word with highlighting
    """
    if es.ping() is False:
        raise Exception("Elastic is not available")
    else:
        result_list = []

        content = graphql_query(query_all_data_by_uid(uid, is_startpoint))

        if not content:
            return result_list

        if not es.indices.exists(index="post_statements"):
            es.indices.create(index="post_statements")

        index_query_result_text_versions(es, content.get("statements"))

        search = shape_search_string(search)

        query = query_string_by_whitespace(search)

        search_results = search_in_statements_with_query(es, query)

        if es.indices.exists(index="post_statements"):
            es.indices.delete(index="post_statements")

        for result in search_results.get("hits").get("hits"):
            result_list.append(result.get("highlight").get("content")[0])

        return result_list


def get_all_matching_statements_by_uid_and_synonyms_OLD(es, uid, search, is_startpoint):
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
        if content:
            language = content.get("statements")[0].get("issues").get("langUid")
        else:
            language = 1

        if language is 1:
            synonym_analyzer = "synonyms_english"
        elif language is 2:
            synonym_analyzer = "synonyms_german"

        if not content:
            return result_list

        settings = setting_string()

        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name,
                              body=settings)
        else:
            es.indices.delete(index=index_name)
            es.indices.create(index=index_name,
                              body=settings)

        if es.indices.exists(index=index_name):

            index_query_result_text_versions(es, content.get("statements"))

            search = shape_search_string(search)

            query = query_string_synonym_text_search(search, synonym_analyzer)

            search_results = search_in_statements_with_query(es, query)

            es.indices.delete(index=index_name)
            for result in search_results.get("hits").get("hits"):
                if "highlight" in result:
                    value = result.get("highlight").get("content")[0]
                    result_list.append(value)

        return result_list


def get_strings_for_suggestion(es, uid, search, is_startpoint):
    results = get_all_matching_statements_by_uid(es, uid, search, is_startpoint)
    content_to_show = []
    for result in results:
        # todo work on second tags
        filling = {"text": "Fits: " + result}
        content_to_show.append(filling)
    return content_to_show


def get_strings_for_suggestion_with_synonyms(es, uid, search, is_startpoint):
    results = get_all_matching_statements_by_uid_and_synonyms(es, uid, search, is_startpoint)
    print(results)
    content_to_show = []
    for result in results:
        # todo work on second tags
        filling = {"text": "Fits: " + result}
        content_to_show.append(filling)
    return content_to_show


def get_all_issue_uids():
    issue_ids = []
    uids = graphql_query(query_all_uids())

    for id in uids.get("issues"):
        if id not in issue_ids:
            issue_ids.append(id.get("uid"))

    return issue_ids


def get_all_data_of_active_issues():
    statements = []

    issue_ids = get_all_issue_uids()
    for id in issue_ids:
        content = graphql_query(query_every_datas_from_active_issue(id))
        content = content.get("statements")
        if content:
            for data in content:
                statements.append(data)

    return statements


def create_elastic_search_connection():
    """

    :return: new instance of the elastic client
    """

    es = Elasticsearch([{"host": ELASTIC_SEARCH_ADDRESS, "port": ELASTIC_SEARCH_PORT}])

    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)

    # indexing part
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME,
                          body=setting_string())

    content = get_all_data_of_active_issues()
    for i in range(len(content)):
        es.index(index=INDEX_NAME,
                 doc_type="json",
                 id=i,
                 body=content[i])
    es.indices.refresh(index=INDEX_NAME)

    return es


def get_language_of_issue(uid):
    return graphql_query(query_language_of_issue_by_uid(uid)).get("issue").get("languages").get("uiLocales")


def get_all_matching_statements_by_uid_and_synonyms(es, uid, search, is_startpoint):
    results = []

    language = get_language_of_issue(uid)
    synonym_analyzer = FILTER.get(language)

    if es.ping() is False:
        raise Exception("Elastic is not available")
    else:
        query = query_search(search, uid, is_startpoint, synonym_analyzer)
        search_results = es.search(index=INDEX_NAME, body=query)
        for result in search_results.get("hits").get("hits"):
            if "highlight" in result:
                results.append(result.get("highlight").get("textversions.content")[0])
    return results
