import random
import string
import time
import unittest

from search_service import DBAS_PROTOCOL, DBAS_PORT, DBAS_HOST
from search_service.elastic.search import create_connection, init_database, get_suggestions


class TestSeeding(unittest.TestCase):

    @staticmethod
    def id_generator(size=6):
        chars = string.ascii_lowercase
        return "".join(random.choice(chars) for _ in range(size))

    def setUp(self):
        self.es = create_connection()
        time.sleep(8)

    def test_seeding_works(self):
        """
        Test if seeding with correct env-vars works.

        :return:
        """
        index = self.id_generator()
        try:
            init_database(self.es, DBAS_PROTOCOL, DBAS_HOST, DBAS_PORT, index)
        except (Exception, ConnectionError):
            self.fail("init_data base failed")
        res = get_suggestions(self.es, 2, "cat", True)
        self.assertGreater(len(res), 0)

    def test_seeding_fails_1(self):
        """
        Test if seeding with wrong Protocol fails.

        :return:
        """
        index = self.id_generator()
        try:
            init_database(self.es, "coconut", DBAS_HOST, DBAS_PORT, index)
            self.fail("The database should not be initialized")
        except (Exception, ConnectionError):
            pass

    def test_seeding_fails_2(self):
        """
        Test if seeding with wrong Host fails.

        :return:
        """
        index = self.id_generator()
        try:
            init_database(self.es, DBAS_PROTOCOL, "cockatoo", DBAS_PORT, index)
            self.fail("The database should not be initialized")
        except (Exception, ConnectionError):
            pass

    def test_seeding_fails_3(self):
        """
        Test if seeding with wrong Port fails.

        :return:
        """
        index = self.id_generator()
        try:
            init_database(self.es, DBAS_PROTOCOL, DBAS_HOST, "seagull", index)
            self.fail("The database should not be initialized")
        except (Exception, ConnectionError):
            pass

    def test_seeding_fails_4(self):
        """
        Test if seeding only with correct Port fails.

        :return:
        """
        index = self.id_generator()
        try:
            init_database(self.es, "coconut", "cockatoo", DBAS_PORT, index)
            self.fail("The database should not be initialized")
        except (Exception, ConnectionError):
            pass

    def test_seeding_fails_5(self):
        """
        Test if seeding only with correct Host fails.

        :return:
        """
        index = self.id_generator()
        try:
            init_database(self.es, "coconut", DBAS_HOST, "seagull", index)
            self.fail("The database should not be initialized")
        except (Exception, ConnectionError):
            pass

    def test_seeding_fails_6(self):
        """
        Test if seeding only with correct Protocol fails.

        :return:
        """
        index = self.id_generator()
        try:
            init_database(self.es, DBAS_PROTOCOL, "cockatoo", "seagull", index)
            self.fail("The database should not be initialized")
        except (Exception, ConnectionError):
            pass
