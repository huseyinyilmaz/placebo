"""Tests for main http."""
import json
import unittest
import requests
from placebo import Placebo
from placebo.backends import httmockbackend


class BaseMock(Placebo):
    backend = httmockbackend.get_decorator


class GetMock(BaseMock):

    item = {'name': 'Huseyin', 'last_name': 'Yilmaz'}

    # Rest of the attributes are from Placebo interface
    url = 'http://www.example.com/api/item'
    status = 200
    body = json.dumps(item)
    headers = {'content-type': 'application/json',
               'custom-header': 'OK'}


class StringValuesTestCase(unittest.TestCase):

    @GetMock.decorate
    def test_get(self):
        response = requests.get(GetMock.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), GetMock.item)
        self.assertEqual(response.headers, GetMock.headers)

    @GetMock.decorate(status=500)
    def test_update_status(self):
        response = requests.get(GetMock.url)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), GetMock.item)
        self.assertEqual(response.headers, GetMock.headers)
