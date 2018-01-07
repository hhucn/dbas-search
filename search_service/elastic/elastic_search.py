from elasticsearch import Elasticsearch

from search_service import ELASTIC_SEARCH_ADDRESS, ELASTIC_SEARCH_PORT
from search_service import INDEX_NAME, DOC_TYPE, FILTER
from search_service.database_handling.query_with_graphql import graphql_query, query_every_datas_from_active_issue, \
    query_language_of_issue_by_uid, query_all_uids
from search_service.elastic.elastic_search_helper import setting_string, query_search, query_exact_term, data_mapping


def create_connection():
    """

    :return: new instance of the elastic client
    """

    return Elasticsearch([{"host": ELASTIC_SEARCH_ADDRESS, "port": ELASTIC_SEARCH_PORT}])


def get_suggestions(es, uid, search, is_startpoint):
    results = get_matching_statements(es, uid, search, is_startpoint)
    content_to_show = []
    for result in results:
        filling = {"text": result}
        content_to_show.append(filling)
    return content_to_show


def get_every_issue_id():
    issue_ids = []
    uids = graphql_query(query_all_uids())

    for id in uids.get("issues"):
        if id not in issue_ids:
            issue_ids.append(id.get("uid"))

    return issue_ids


def get_data_of_issues():
    statements = []

    issue_ids = get_every_issue_id()
    for id in issue_ids:
        content = graphql_query(query_every_datas_from_active_issue(id))
        content = content.get("statements")
        if content:
            for data in content:
                statements.append(data)

    return statements


def init_database():
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

    content = get_data_of_issues()
    for i in range(len(content)):
        es.index(index=INDEX_NAME,
                 doc_type=DOC_TYPE,
                 id=i,
                 body=content[i])
    es.indices.refresh(index=INDEX_NAME)

    return es


def get_language_of_issue(uid):
    query = query_language_of_issue_by_uid(uid)
    result = graphql_query(query)
    language = result.get("issue").get("languages").get("uiLocales")
    return language


def get_matching_statements(es, uid, search, is_startpoint):
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


def search_result_length(es, search):
    where = "textversions.content"
    query = query_exact_term(search, where)
    res = es.search(index=INDEX_NAME, body=query)
    return len(res.get("hits").get("hits"))


def get_existence(es, search):
    res = search_result_length(es, search)
    return True if res is 1 else False


def get_length_of_index(es):
    dump = es.search(index=[INDEX_NAME], doc_type=[DOC_TYPE], size=10000)
    length = dump.get('hits').get('total')
    return length


def insert_data_to_index(es, text, is_startpoint, uid, langUid):
    exists = get_existence(es, text)
    if not exists:
        length = get_length_of_index(es)
        es.index(index=INDEX_NAME,
                 doc_type=DOC_TYPE,
                 id=length,
                 body=data_mapping(text, is_startpoint, uid, langUid))
        es.indices.refresh(index=INDEX_NAME)
    else:
        print("Already in Database")


def get_availability():
    es = Elasticsearch([{"host": ELASTIC_SEARCH_ADDRESS, "port": ELASTIC_SEARCH_PORT}])
    return es.ping()