import unittest

import requests


class TestInterface(unittest.TestCase):
    def test_flask_send_response(self):
        # notice that flask must run for a passing test!
        response = requests.get('http://0.0.0.0:5000/get_suggestions?id=1')
        self.assertEqual(response.status_code, 200)

    def test_flask_send_json1(self):
        response = requests.get('http://0.0.0.0:5000/get_suggestions?id=1')
        self.assertIsNotNone(response.json()[0])

    def test_flask_send_json2(self):
        response = requests.get('http://0.0.0.0:5000/get_suggestions?id=1&search=hi')
        self.assertIsNotNone(response.json()[0])

    def test_flask_send_json3(self):
        response = requests.get('http://0.0.0.0:5000/get_suggestions?id=2&search=hi&start=false')
        self.assertIsNotNone(response.json()[0])

    def test_flask_send_json4(self):
        response = requests.get('http://0.0.0.0:5000/get_suggestions?search=&start=true')
        self.assertIsNotNone(response.json()[0])
