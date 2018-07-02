import unittest

from search_service.database.query_with_graphql import json_to_dict


class TestJsonToDict(unittest.TestCase):

    def test_dict_to_dict(self):
        """
        Test json_to_dict returns dict if the input is a dict.

        :return:
        """
        dictionary = {"coconut": "seagull"}
        res = json_to_dict(dictionary)
        self.assertEqual(type(res), dict)

    def test_bytes_to_dict(self):
        """
        Test json_to_dict returns dict if the input is a byte.

        :return:
        """
        dictionary = b'{"coconut": "seagull"}'
        res = json_to_dict(dictionary)
        self.assertEqual(type(res), dict)
