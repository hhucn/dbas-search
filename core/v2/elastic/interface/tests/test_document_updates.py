import time
import unittest

from core import STATEMENT_INDEX, DOC_TYPE
from core.v2.elastic.interface.es_interface import ESInterface
from core.v2.elastic.queries.es_query import ESQuery


class TestDocumentUpdate(unittest.TestCase):

    def setUp(self):
        self.index = STATEMENT_INDEX
        self.es_client = ESInterface(index=self.index)
        time.sleep(3)

    def test_textversion_is_updated(self):
        body = {
            "issue_uid": 2,
            "slug": "coco-nut",
            "ui_locales": "en",
            "title": "coconut",
            "info": "Coconut ooooh cocococococnut",
            "author_uid": 1,
            "public_nickname": "Coconut",
            "is_position": True,
            "uid": 2,
            "content": "Coconuts are great"
        }

        update_ack = self.es_client.update_document(
            body=ESQuery().update_textversion_information(
                statement_uid=body.get("uid"),
                element=body),
            doc_type=DOC_TYPE
        )
        self.assertEqual(update_ack.get("failures"), [])
        self.assertGreater(update_ack.get("total"), 0)

    def test_issue_is_updated(self):
        body = {
            "issue_uid": 2,
            "slug": "coco-nut",
            "ui_locales": "en",
            "title": "coconut",
            "info": "Coconut ooooh cocococococnut"
        }

        update_ack = self.es_client.update_document(
            body=ESQuery().update_issue_information(
                issue_uid=body.get("issue_uid"),
                element=body),
            doc_type=DOC_TYPE
        )
        self.assertEqual(update_ack.get("failures"), [])
        self.assertGreater(update_ack.get("total"), 0)

    def test_author_is_updated(self):
        body = {
            "author_uid": 1,
            "public_nickname": "Coconut"
        }

        update_ack = self.es_client.update_document(
            body=ESQuery().update_author_information(
                author_uid=body.get("author_uid"),
                element=body
            ),
            doc_type=DOC_TYPE
        )
        self.assertEqual(update_ack.get("failures"), [])
        self.assertGreater(update_ack.get("total"), 0)

    def test_statement_is_updated(self):
        update_ack = self.es_client.update_document(
            body=ESQuery().update_statement_information(
                statement_uid=1,
                is_position=True
            ),
            doc_type=DOC_TYPE
        )
        self.assertEqual(update_ack.get("failures"), [])
        self.assertGreater(update_ack.get("total"), 0)
