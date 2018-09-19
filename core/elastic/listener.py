import json
import os
import threading
import time

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from core import V1_DB_INDEX, DOC_TYPE
from core.database.query_with_graphql import query_statement_info_by_issue_uid, send_request_to_graphql
from core.elastic.query_strings import data_mapping, update_textversion, update_issue, update_statement
from core.v1.search import create_connection, index_new_element
from core.v2.elastic.mechanics.es_connector import ESConnector


def __listen_to_db():
    """
    Listen to the postgresql database of DBAS.
    Listen especially to textversions_changes and index the incoming data to the elastic search index.

    :return:
    """
    conn = psycopg2.connect(user=os.environ["DATABASE_USER"], password=os.environ["DATABASE_PASSWORD"],
                            database=os.environ["DATABASE_NAME"], host=os.environ["DATABASE_HOST"])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    commands = ["LISTEN issues_changes;", "LISTEN textversions_changes;", "LISTEN statements_changes;"]
    for command in commands:
        curs.execute(command)
    while True:
        conn.poll()
        time.sleep(0.5)
        while conn.notifies:
            notify = conn.notifies.pop(0)
            notification = json.loads(notify.payload)

            if notification["event"] == "insert_textversions":
                __insert_new_data(notification)

            elif notification["event"] == "update_textversions":
                __update_textversion(notification)

            elif notification["event"] == "update_issues":
                __update_issue(notification)

            elif notification["event"] == "update_statements":
                __update_statement(notification)


def __insert_new_data(notification: dict):
    """
    Insert and index the data delivered in notification to the elastic search index.
    Add additional information to the insertion datas.
    Additional information are: statement.isPosition, issue.uid, issue.langUid.

    :param notification: incoming notification containing the inserted data
    :return:
    """
    statement_uid = notification["data"]["statement_uid"]
    content = notification["data"]["content"]
    query = query_statement_info_by_issue_uid(statement_uid)
    response = send_request_to_graphql(query)
    position = response["statement"]["isPosition"]
    issue_uid = response["statement"]["issueUid"]
    lang_uid = response["statement"]["lang"]
    results = data_mapping(content, position, issue_uid, lang_uid, statement_uid)
    es = create_connection()
    index_new_element(es, results)


def __update_textversion(notification: dict):
    """
    Updates an existing element by its statement_uid.

    :param notification:
    :return:
    """

    statement_uid = notification.get("data").get("statement_uid")
    content = notification.get("data").get("content")
    query = query_statement_info_by_issue_uid(statement_uid)
    response = send_request_to_graphql(query)
    position = response.get("statement").get("isPosition")
    issue_uid = response.get("statement").get("issueUid")
    lang_uid = response.get("statement").get("lang")
    element = data_mapping(text=content, is_position=position, uid=issue_uid, language=lang_uid,
                           statement_uid=statement_uid)
    query = update_textversion(
        element=element
    )
    es_client = ESConnector(index=V1_DB_INDEX)
    es_client.update_document(
        body=query,
        doc_type=DOC_TYPE
    )


def __update_issue(notification: dict):
    """
    Updates an existing element by its issue_uid.

    :param notification:
    :return:
    """
    issue_uid = notification.get("data").get("uid")
    query = query_statement_info_by_issue_uid(issue_uid)
    response = send_request_to_graphql(query)
    lang = response.get("statement").get("lang")
    element = data_mapping(text=str(), is_position=bool(), uid=issue_uid, language=lang, statement_uid=int())

    query = update_issue(
        element=element
    )
    es_client = ESConnector(index=V1_DB_INDEX)
    es_client.update_document(
        body=query,
        doc_type=DOC_TYPE
    )


def __update_statement(notification: dict):
    """
    Updates an existing element by its statement uid.

    :param notification:
    :return:
    """
    statement_uid = notification.get("data").get("uid")
    is_position = notification.get("data").get("is_position")
    element = data_mapping(text=str(), is_position=is_position, uid=int(), language=str(), statement_uid=statement_uid)
    query = update_statement(
        element=element
    )
    es_client = ESConnector(index=V1_DB_INDEX)
    es_client.update_document(
        body=query,
        doc_type=DOC_TYPE
    )


def start_listening():
    """
    Start the postgresql database listener of the DBAS database in background.
    This listener will also insert incoming data to the elastic search index.

    :return:
    """
    t1 = threading.Thread(target=__listen_to_db)
    t1.start()
