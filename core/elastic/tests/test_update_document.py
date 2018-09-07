import time
import unittest

from core import V1_DB_INDEX, DOC_TYPE
from core.elastic.query_strings import data_mapping, update_textversion, update_issue, update_statement
from core.v2.elastic.mechanics.es_connector import ESConnector


class TestDocumentUpdate(unittest.TestCase):

    def setUp(self):
        self.es_client = ESConnector(index=V1_DB_INDEX)
        time.sleep(3)

    def test_if_textversion_is_updated(self):
        notification = data_mapping(text="Coconut", is_position=True, uid=1, lang_id="en", statement_uid=2)
        query = update_textversion(element=notification)
        update_ack = self.es_client.update_document(
            body=query,
            doc_type=DOC_TYPE
        )
        self.assertEqual(update_ack.get("failures"), [])

    def test_if_issue_is_updated(self):
        notification = data_mapping(text=None, is_position=None, uid=2, lang_id="de", statement_uid=None)
        query = update_issue(element=notification)
        update_ack = self.es_client.update_document(
            body=query,
            doc_type=DOC_TYPE
        )
        self.assertEqual(update_ack.get("failures"), [])

    def test_if_statement_is_updated(self):
        notification = data_mapping(text=None, is_position=False, uid=None, lang_id=None, statement_uid=2)
        query = update_statement(element=notification)
        update_ack = self.es_client.update_document(
            body=query,
            doc_type=DOC_TYPE
        )
        self.assertEqual(update_ack.get("failures"), [])
