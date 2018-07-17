import unittest

from core.v2.sql.db_interface.db_interface import DBInterface
from core.v2.sql.db_models.author import Author
from core.v2.sql.db_models.issue import Issue
from core.v2.sql.db_models.statement import Statement


class TestModels(unittest.TestCase):
    def setUp(self):
        self.inter = DBInterface(file='request.sql')
        self.result = self.inter.query_data_with_sql()

    def test_statement_is_created_properly(self):
        keys = ['uid', 'isPosition', 'text']
        for res in self.result:
            statement = Statement(content=res)
            self.assertIsNotNone(statement)
            self.assertIsNotNone(statement.__json__())
            for key in keys:
                self.assertTrue(key in statement.__json__().keys())

    def test_issue_is_created_properly(self):
        keys = ['uid', 'slug', 'lang', 'title', 'info']
        for res in self.result:
            issue = Issue(content=res)
            self.assertIsNotNone(issue)
            self.assertIsNotNone(issue.__json__())
            for key in keys:
                self.assertTrue(key in issue.__json__().keys())

    def test_author_is_created_properly(self):
        keys = ['uid', 'nickname']
        for res in self.result:
            author = Author(content=res)
            self.assertIsNotNone(author)
            self.assertIsNotNone(author.__json__())
            for key in keys:
                self.assertTrue(key in author.__json__().keys())
