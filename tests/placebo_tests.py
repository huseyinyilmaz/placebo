"""Tests for main placebo interface and functionality."""
import json
import unittest
import requests
from tests import utils


class GetMock(utils.BasePlacebo):
    # Test related data. Not part of the interface.
    item = {'name': 'Huseyin', 'last_name': 'Yilmaz'}
    item2 = {'name': 'Mert', 'last_name': 'Yilmaz'}
    url2 = 'http://www.example2.com/api/item'
    headers2 = {'custom-header': 'headers2',
                'another-header': 'some data'}

    # Data for placebo interface
    url = 'http://www.example.com/api/item'
    body = json.dumps(item)
    headers = {'custom-header': 'OK',
               'custom-header2': 'Second header'}


class StringValuesTestCase(unittest.TestCase):

    def assertHeadersEqual(self, heads_a, heads_b):
        """Do not test for common headers for httpretty.

        Since httpretty is a socket level library, other libraries
        before the socket adds common headers. So we are removing
        common headers for httpretty.
        """
        if utils.is_httpretty:
            heads_a = utils.remove_common_headers(heads_a)
            heads_b = utils.remove_common_headers(heads_b)

        self.assertEqual(heads_a, heads_b)

    @GetMock.decorate
    def test_base_call(self):
        response = requests.get(GetMock.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), GetMock.item)
        self.assertHeadersEqual(response.headers, GetMock.headers)

    @GetMock.decorate(status=500)
    def test_update_status(self):
        response = requests.get(GetMock.url)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), GetMock.item)
        self.assertHeadersEqual(response.headers, GetMock.headers)

    @GetMock.decorate(method='POST')
    def test_update_method(self):
        response = requests.post(GetMock.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), GetMock.item)
        self.assertHeadersEqual(response.headers, GetMock.headers)

    @GetMock.decorate(url=GetMock.url2)
    def test_update_url(self):
        response = requests.get(GetMock.url2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), GetMock.item)
        self.assertHeadersEqual(response.headers, GetMock.headers)

    @GetMock.decorate(headers=GetMock.headers2)
    def test_update_headers(self):
        response = requests.get(GetMock.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), GetMock.item)
        self.assertHeadersEqual(response.headers, GetMock.headers2)

    @GetMock.decorate(body=json.dumps(GetMock.item2))
    def test_update_body(self):
        response = requests.get(GetMock.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), GetMock.item2)
        self.assertHeadersEqual(response.headers, GetMock.headers)

    @GetMock.decorate
    @GetMock.decorate(url=GetMock.url2,
                      method='POST',
                      body=json.dumps(GetMock.item2),
                      headers=GetMock.headers2,
                      status=500)
    def test_multiple_decorators(self):
        # test first decorator data
        response = requests.get(GetMock.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), GetMock.item)
        if not utils.is_httpretty:
            self.assertHeadersEqual(response.headers, GetMock.headers)
        # test second decorator data
        response2 = requests.post(GetMock.url2)
        self.assertEqual(response2.status_code, 500)
        self.assertEqual(response2.json(), GetMock.item2)
        if not utils.is_httpretty:
            self.assertEqual(response2.headers, GetMock.headers2)

    @GetMock.decorate
    @GetMock.decorate(url=GetMock.url,
                      method='POST',
                      body=json.dumps(GetMock.item2),
                      headers=GetMock.headers2,
                      status=500)
    def test_decorate_post_and_get_of_same_url(self):
        # test first decorator data
        response = requests.get(GetMock.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), GetMock.item)
        if not utils.is_httpretty:
            self.assertHeadersEqual(response.headers, GetMock.headers)
        # test second decorator data
        response2 = requests.post(GetMock.url)
        self.assertEqual(response2.status_code, 500)
        self.assertEqual(response2.json(), GetMock.item2)
        if not utils.is_httpretty:
            self.assertEqual(response2.headers, GetMock.headers2)
