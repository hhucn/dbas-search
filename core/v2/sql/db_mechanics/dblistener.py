import json
import logging
import time
from threading import Thread

from elasticsearch import TransportError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from core import DOC_TYPE
from core.database.query_with_graphql import send_request_to_graphql, query_language_of_issue
from core.v2.elastic.interface.es_interface import ESInterface
from core.v2.elastic.mapping.mapping import Mapping
from core.v2.elastic.queries.es_query import ESQuery
from core.v2.sql.db_interface.db_interface import DBInterface
from core.v2.sql.db_mechanics.dbconnector import DBConnector
from core.v2.sql.db_models.author import Author
from core.v2.sql.db_models.issue import Issue
from core.v2.sql.db_models.statement import Statement


class DBListener(Thread):
    """
    This class is a database listener.
    It can listen to specific database event.
    The DBListener also updates or inserts new elements if it notifies a database message.
    """

    def __init__(self, index: str, commands: list, refresh_time: int = 0.5):
        Thread.__init__(self)
        self.commands = commands
        self.db_client = DBConnector()
        self.refresh_time = refresh_time
        self.index = index

    def handle_textversions_payload(self, payload):
        """
        This method updates a the textversion of an specific document.

        :param payload: payload that contains the new elements, must match Statement, Author, Issue
        :return:
        """
        if "textversions" in payload.get("event"):
            sql = DBInterface(file='additional_textversion.sql').read_file().format(
                payload.get("data").get("statement_uid"),
                payload.get("data").get("author_uid"))
            results = DBConnector().query(query=sql)
            es_client = ESInterface(index=self.index)
            if payload.get("event") == "update_textversions":
                for content in results:
                    es_client.update_document(
                        body=ESQuery().update_textversion_information(
                            statement_uid=payload.get("data").get("statement_uid"),
                            element=content),
                        doc_type=DOC_TYPE)
            elif payload.get("event") == "insert_textversions":
                for content in results:
                    statement = Statement(content)
                    author = Author(content)
                    issue = Issue(content)
                    data = Mapping.data_mapping(statement, author, issue)
                    es_client.index_element(data)

    def handle_issues_payload(self, payload):
        """
        This method updates a the issue of an specific document.

        :param payload: payload that contains the new elements, must match Issue
        :return:
        """
        if "issues" in payload.get("event"):
            es_client = ESInterface(index=self.index)
            results = send_request_to_graphql(query=query_language_of_issue(payload.get("data").get("uid")))
            payload_mod = dict(payload.get("data"))
            payload_mod.update({"ui_locales": results.get("issue").get("languages").get("uiLocales")})
            payload_mod.update({"issue_uid": payload.get("data").get("uid")})
            if payload.get("event") == "update_issues":
                es_client.update_document(
                    body=ESQuery().update_issue_information(
                        issue_uid=payload_mod.get("uid"),
                        element=payload_mod),
                    doc_type=DOC_TYPE)

    def handle_user_payload(self, payload):
        """
        This method updates a the author of an specific document.

        :param payload: payload that contains the new elements, must match Author
        :return:
        """
        if "users" in payload.get("event"):
            es_client = ESInterface(index=self.index)
            payload_mod = dict(payload.get("data"))
            payload_mod.update({"author_uid": payload.get("data").get("uid")})
            es_client.update_document(
                body=ESQuery().update_author_information(
                    author_uid=payload_mod.get("uid"),
                    element=payload_mod),
                doc_type=DOC_TYPE)

    def handle_statement_payload(self, payload):
        """
        This method updates a the statement of an specific document.

        :param payload: payload that contains the new elements, must match Statement
        :return:
        """
        if "statements" in payload.get("event"):
            es_client = ESInterface(index=self.index)
            es_client.update_document(
                body=ESQuery().update_statement_information(
                    statement_uid=payload.get("data").get("uid"),
                    is_position=payload.get("data").get("is_position")
                ),
                doc_type=DOC_TYPE)

    def run(self):
        """
        Listen to the specific database events defined in commands.

        :return:
        """
        try:
            self.db_client.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            for command in self.commands:
                self.db_client.curs.execute(command)
            while True:
                self.db_client.conn.poll()
                time.sleep(self.refresh_time)
                while self.db_client.conn.notifies:
                    notification = self.db_client.conn.notifies.pop(0)
                    payload = json.loads(notification.payload)
                    self.handle_textversions_payload(payload)
                    self.handle_issues_payload(payload)
                    self.handle_user_payload(payload)
                    self.handle_statement_payload(payload)
        except TransportError as err:
            logging.error(err)
