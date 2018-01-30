"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
from elasticsearch import Elasticsearch

from search_service import INDEX_NAME, DOC_TYPE, FILTER
from search_service.database.query_with_graphql import send_request_to_graphql, query_data_of_issue, \
    query_language_of_issue, query_all_uid
from search_service.elastic.query_strings import settings, search_query, query_exact_term, data_mapping, edits_query
import logging


def create_connection():
    """

    :return: connection to elasticsearch-client
    """
    return Elasticsearch([{"host": "0.0.0.0", "port": 9200}])


def init_database(es):
    """
    Fills the elasticsaerch database with all data of active issues.

    :param es: active client of elasticsearch
    :return:
    """
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)

    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME,
                          body=settings())

    content = get_data_of_issues()
    for i in range(len(content)):
        es.index(index=INDEX_NAME,
                 doc_type=DOC_TYPE,
                 id=i,
                 body=content[i])
    es.indices.refresh(index=INDEX_NAME)


def append_data(es, text, uid, start_point):
    """
    Append to the database.
    The data_mapping is the common used data format of the database.

    :param es: active client of elasticsearch
    :param text: the text to be appended (text)
    :param uid: the uid of the current issue (int)
    :param start_point: is the text a start point or not (boolean)
    :param lang_id: the id of the language (int)
    :return:
    """
    language = get_used_language(uid)
    lang_id = 1 if language is "en" else 2
    exists = get_existence(es, text)
    if not exists:
        length = get_index_length(es)
        es.index(index=INDEX_NAME,
                 doc_type=DOC_TYPE,
                 id=length,
                 body=data_mapping(text, start_point, uid, lang_id))
        es.indices.refresh(index=INDEX_NAME)
    else:
        logging.debug("Already in Database")


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
    return prepare_content_list(results)


def get_edits(es, uid, search):
    """
    Returns a dictionary with suggestions for the edit popup.
    Notice that the content strings are already customized with highlighting strings.

    :param es: active client of elasticsearch
    :param uid: the uid of the current issue (int)
    :param search: the text to be looked up (string)
    :param start_point: look up in start points or not (boolean)
    :return:
    """
    results = get_matching_edits(es, uid, search)
    return prepare_content_list(results)


def prepare_content_list(results):
    """
    Returns a prepared list to use it at the frontend.

    :param results:
    :return:
    """
    content_to_show = []
    for result in results:
        filling = {"text": result}
        content_to_show.append(filling)
    return content_to_show


def get_every_issue_id():
    """

    :return: every uid in the D-BAS database
    """
    issue_ids = []
    uids = send_request_to_graphql(query_all_uid())

    for id in uids.get("issues"):
        if id not in issue_ids:
            issue_ids.append(id.get("uid"))

    return issue_ids


def get_data_of_issues():
    """

    :return: every data in the D-BAS database
    """
    statements = []

    issue_ids = get_every_issue_id()
    for id in issue_ids:
        content = send_request_to_graphql(query_data_of_issue(id))
        content = content.get("statements")
        if content:
            for data in content:
                statements.append(data)

    return statements


def get_used_language(uid):
    """
    Determine the language of a issue.

    :param uid: current issue id (int)
    :return: determined language of the current issue
    """
    query = query_language_of_issue(uid)
    result = send_request_to_graphql(query)
    language = result.get("issue").get("languages").get("uiLocales")
    return language


def get_matching_statements(es, uid, search, start_point):
    """
    Returns a list with suggestions.
    Notice that the content strings are already customized with highlighting strings.

    :param es: active client of elasticsearch
    :param uid: current issue id (int)
    :param search: the text to be looked up (string)
    :param start_point: look up in start points or not (boolean)
    :return:
    """

    language = get_used_language(uid)
    synonym_analyzer = FILTER.get(language)
    return search_with_query(es, search_query(search, uid, start_point, synonym_analyzer))


def get_matching_edits(es, uid, search):
    """
    Returns a list with suggestions for edit statements.

    :param es: active client of elasticsearch
    :param uid: current issue id (int)
    :param search: the text to be looked up (string)
    :return:
    """
    language = get_used_language(uid)
    synonym_analyzer = FILTER.get(language)
    return search_with_query(es, edits_query(search, uid, synonym_analyzer))


def search_with_query(es, query_string):
    results = []

    if es.ping() is False:
        raise Exception("Elastic is not available")
    else:
        query = query_string
        search_results = es.search(index=INDEX_NAME, body=query)
        for result in search_results.get("hits").get("hits"):
            if "highlight" in result:
                results.append(result.get("highlight").get("textversions.content")[0])
    return results


def get_result_length(es, search):
    """
    Used to determine the existence of a text.

    :param es: active client of elasticsearch
    :param search: the text to be looked up (string)
    :return: length of the search results to check existence of search
    """
    where = "textversions.content"
    query = query_exact_term(search, where)
    res = es.search(index=INDEX_NAME, body=query)
    return len(res.get("hits").get("hits"))


def get_existence(es, search):
    """
    Determine the existence of a text which should be inserted to the database.

    :param es: active client of elasticseach
    :param search: the text to be looked up (string)
    :return: the existence of a search text
    """
    res = get_result_length(es, search)
    return res is 1


def get_index_length(es):
    """
    The length of the database to append new data.

    :param es: active client of elasticsearch
    :return: length of database
    """
    dump = es.search(index=[INDEX_NAME], doc_type=[DOC_TYPE], size=10000)
    length = dump.get('hits').get('total')
    return length


def get_availability():
    """

    :return: the availability of elasticsearch
    """
    es = create_connection()
    return es.ping()
