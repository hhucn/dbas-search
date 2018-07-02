"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""

from elasticsearch import Elasticsearch

from search_service import INDEX_NAME, DOC_TYPE, FILTER
from search_service.database.query_with_graphql import send_request_to_graphql, query_data_of_issue, \
    query_language_of_issue, query_all_uid
from search_service.elastic.query_strings import settings, edits_query, search_query, \
    duplicates_or_reasons_query, all_statements_with_value_query, data_mapping


def create_connection():
    """

    :return: connection to elasticsearch-client
    """
    return Elasticsearch([{"host": "0.0.0.0", "port": 9200}])


def init_database(es, protocol, host, port):
    """
    Fills the elasticsearch database with all data of active issues.

    :param port:
    :param host:
    :param protocol:
    :param es: active client of elasticsearch
    :return:
    """
    if not (es.indices.exists(index=INDEX_NAME)):
        es.indices.create(index=INDEX_NAME, body=settings(), ignore=[400, 503])
        for content in __get_data_of_issues(protocol, host, port):
            index_new_element(es, __map_data(content))
        es.indices.refresh(index=INDEX_NAME)


def __map_data(content):
    """
    Maps a given content to the data structure that elastic requires.

    :param content: data to be mapped
    :return: data in required data structure
    """
    text = content["textversions"]["content"]
    statement_uid = content["textversions"]["statementUid"]
    is_position = content["isPosition"]
    issue_uid = content["issueUid"]
    language = content["lang"]
    return data_mapping(text, is_position, issue_uid, language, statement_uid)


def get_suggestions(es, uid, search, start_point):
    """
    Returns a dictionary with suggestions.
    Notice that the content strings are already customized with highlighting strings.

    :param es: active client of elasticsearch
    :param uid: the uid of the current issue (int)
    :param search: the text to be looked up (string)
    :param start_point: look up in start points or not (boolean)
    :return:
    """
    results = get_matching_statements(es, uid, search, start_point)
    return __prepare_content_list(results)


def get_edits(es, uid, statement_uid, search):
    """
    Returns a dictionary with suggestions for the edit popup.
    Notice that the content strings are already customized with highlighting strings.

    :param es: active client of elasticsearch
    :param uid: the uid of the current issue (int)
    :param search: the text to be looked up (string)
    :param statement_uid: is the statementUid
    :return:
    """
    results = __get_matching_edits(es, uid, statement_uid, search)
    return __prepare_content_list(results)


def get_duplicates_or_reasons(es, uid, statement_uid, search):
    results = __get_matching_duplicates_or_reasons(es, uid, statement_uid, search)
    return __prepare_content_list(results)


def get_all_statements_with_value(es, search, uid):
    results = __get_matching_statements_with_value(es, uid, search)
    return __prepare_content_list(results)


def get_availability():
    """
    
    :return: the availability of elasticsearch
    """
    es = create_connection()
    return es.ping()


def get_matching_statements(es, uid, search, position):
    """
    Returns a list with suggestions.
    Notice that the content strings are already customized with highlighting strings.
    
    :param es: active client of elasticsearch
    :param uid: current issue id (int)
    :param search: the text to be looked up (string)
    :param position: look up in start points or not (boolean)
    :return:
    """

    language = __get_used_language(uid)
    synonym_analyzer = FILTER.get(language)
    return __search_with_query(es, search_query(search, uid, position, synonym_analyzer))


def index_new_element(es, content):
    es.index(index=INDEX_NAME,
             doc_type=DOC_TYPE,
             body=content)


def __get_issue_ids(protocol, host, port):
    """

    :return: every uid in the D-BAS database
    """
    uids = send_request_to_graphql(query_all_uid(), protocol, host, port)
    if uids:
        return [id.get("uid") for id in uids.get("issues")]

    return []


def __get_data_of_issues(protocol, host, port):
    """

    :return: every data in the D-BAS database
    """
    statements = []

    issue_ids = __get_issue_ids(protocol, host, port)
    for id in issue_ids:
        content = send_request_to_graphql(query_data_of_issue(id), protocol, host, port)
        content = content.get("statements")
        if content:
            for data in content:
                statements.append(data)

    return statements


def __get_used_language(uid):
    """
    Determine the language of a issue.

    :param uid: current issue id (int)
    :return: determined language of the current issue
    """
    query = query_language_of_issue(uid)
    result = send_request_to_graphql(query)
    language = result.get("issue").get("languages").get("uiLocales")
    return language


def __get_matching_statements_with_value(es, uid, search):
    language = __get_used_language(uid)
    synonym_analyzer = FILTER.get(language)
    return __search_with_query(es, all_statements_with_value_query(search, uid, synonym_analyzer))


def __get_matching_duplicates_or_reasons(es, search, uid, statement_uid):
    language = __get_used_language(uid)
    synonym_analyzer = FILTER.get(language)
    return __search_with_query(es, duplicates_or_reasons_query(search, uid, statement_uid, synonym_analyzer))


def __get_matching_edits(es, uid, statement_uid, search):
    """
    Returns a list with suggestions for edit statements.

    :param es: active client of elasticsearch
    :param uid: current issue id (int)
    :param search: the text to be looked up (string)
    :param statement_uid: to determine the language of the current issue
    :return:
    """
    language = __get_used_language(uid)
    synonym_analyzer = FILTER.get(language)
    return __search_with_query(es, edits_query(search, statement_uid, synonym_analyzer))


def __search_with_query(es, query_string):
    results = []

    if es.ping() is False:
        raise Exception("Elastic is not available")

    query = query_string
    search_results = es.search(index=INDEX_NAME, body=query)
    for result in search_results.get("hits").get("hits"):
        current = []
        if "_source" and "highlight" in result:
            current.append(result["highlight"]["textversions.content"][0])
            current.append(result["_source"]["textversions"]["statementUid"])
            current.append(result["_source"]["textversions"]["content"])
            current.append(result["_score"])
            results.append(current)

    return results


def __prepare_content_list(results):
    """
    Returns a prepared list to use it at the frontend.

    :param results:
    :return:
    """
    return list(map(lambda x: {
        "html": x[0],
        "statement_uid": x[1],
        "text": x[2],
        "score": x[3]
    }, results))
