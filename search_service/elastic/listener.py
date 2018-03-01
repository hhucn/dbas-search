import json
import os
import threading
import time

import psycopg2

from search_service.database.query_with_graphql import query_start_point_issue_of_statement, send_request_to_graphql
from search_service.elastic.query_strings import data_mapping
from search_service.elastic.search import create_connection, index_new_element


def __listen_to_db():
    """
    Listen to the postgresql database of DBAS.
    List in especially to textversions_changes and index the incoming data to the elastic search index.

    :return:
    """
    conn = psycopg2.connect(user=os.environ["DB_USER"], password=os.environ["DB_PW"],
                            database=os.environ["DB_NAME"], host=os.environ["DB_HOST"])
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    curs.execute("LISTEN textversions_changes;")
    while True:
        conn.poll()
        time.sleep(1)
        while conn.notifies:
            notify = conn.notifies.pop(0)
            notification = json.loads(notify.payload)

            if notification["event"] == "insert_textversions":
                __insert_new_data(notification)


def __insert_new_data(notification):
    """
    Insert and index the data delivered in notification to the elastic search index.
    Add additional information to the insertion datas.
    Additional information are: statement.isStartpoint, issue.uid, issue.langUid .

    :param notification: incoming notification containing the inserted data
    :return:
    """
    statement_uid = notification["data"]["statement_uid"]
    content = notification["data"]["content"]
    query = query_start_point_issue_of_statement(statement_uid)
    response = send_request_to_graphql(query)
    is_start_point = response["statement"]["isStartpoint"]
    issue_uid = response["statement"]["issues"]["uid"]
    lang_uid = response["statement"]["issues"]["langUid"]
    results = data_mapping(content, is_start_point, issue_uid, lang_uid, statement_uid)
    es = create_connection()
    index_new_element(es, results)


def start_listening():
    """
    Start the postgresql database listener of the DBAS database in background.
    This listener will also insert incoming data to the elastic search index.

    :return:
    """
    t1 = threading.Thread(target=__listen_to_db)
    t1.start()
