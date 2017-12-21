from elasticsearch import Elasticsearch

from search_service import ELASTIC_SEARCH_ADDRESS, ELASTIC_SEARCH_PORT
from search_service import FILTER
from search_service.database_handling.query_with_graphql import graphql_query, query_every_datas_from_active_issue, \
    query_language_of_issue_by_uid, query_all_uids
from search_service.elastic.elastic_search_helper import setting_string, query_search

INDEX_NAME = "test_index"


def create_elastic_search_client():
    """

    :return: new instance of the elastic client
    """

    return Elasticsearch([{"host": ELASTIC_SEARCH_ADDRESS, "port": ELASTIC_SEARCH_PORT}])


def search_in_statements_with_query(es, query):
    """

    :param es: elastic client
    :param query: query string for the search
    :return results for the elastic search for a string in all of the statements
    """

    return es.search(index="post_statements", doc_type="json", body=query)


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
