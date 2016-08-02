"""Tests for main placebo interface and functionality."""
import json
import unittest
import requests
from placebo import Placebo


class GetMock(Placebo):

    item = {'name': 'Huseyin', 'last_name': 'Yilmaz'}

    url = 'http://www.example.com/api/item'
    body = json.dumps(item)
    headers = {'content-type': 'application/json',
               'custom-header': 'OK'}


class StringValuesTestCase(unittest.TestCase):

    @GetMock.mock
    def test_get(self):
        response = requests.get(GetMock.url)
        self.assertEqual(response.json(), GetMock.item)
        self.assertEqual(response.headers, GetMock.headers)
