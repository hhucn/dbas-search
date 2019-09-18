import random
import string
import time
import unittest

from core import APPLICATION_PROTOCOL, APPLICATION_PORT, APPLICATION_HOST
from core.v1.search import create_connection, init_database


class TestSeeding(unittest.TestCase):

    @staticmethod
    def id_generator(size=6):
        chars = string.ascii_lowercase
        return "".join(random.choice(chars) for _ in range(size))

    def setUp(self):
        self.es = create_connection()
        time.sleep(8)

    def test_seeding_fails_1(self):
        """
        Test if seeding with wrong Protocol fails.

        :return:
        """
        index = self.id_generator()
        try:
            init_database(self.es, "coconut", APPLICATION_HOST, APPLICATION_PORT, index)
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
            init_database(self.es, APPLICATION_PROTOCOL, "cockatoo", APPLICATION_PORT, index)
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
            init_database(self.es, APPLICATION_PROTOCOL, APPLICATION_HOST, "seagull", index)
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
            init_database(self.es, "coconut", "cockatoo", APPLICATION_PORT, index)
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
            init_database(self.es, "coconut", APPLICATION_HOST, "seagull", index)
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
            init_database(self.es, APPLICATION_PROTOCOL, "cockatoo", "seagull", index)
            self.fail("The database should not be initialized")
        except (Exception, ConnectionError):
            pass
