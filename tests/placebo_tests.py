"""Tests for main placebo interface and functionality."""
import json
import re
import unittest
import requests
from tests import utils

from six.moves.urllib import parse


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

###################################
# Regex tests for httmock backend #
###################################


class HttmockCatchAllMock(utils.BasePlacebo):
    item = {'all': True}
    url = parse.ParseResult(
        scheme='',
        netloc=r'.*',
        path='',
        params='',
        query='',
        fragment='')
    body = json.dumps(item)


class HttmockRegexMock(utils.BasePlacebo):
    item = {'name': 'Huseyin', 'last_name': 'Yilmaz'}
    url = parse.ParseResult(
        scheme='',
        netloc=r'^(.*\.)?example\.com$',
        path=r'^/items/(\d+)/$',
        params='',
        query='',
        fragment='')
    body = json.dumps(item)


@unittest.skipUnless(utils.is_httmock,
                     "Httmock specific regex tests")
class HttmockTestCase(unittest.TestCase):
    """Httmock specific tests."""
    @HttmockCatchAllMock.decorate
    @HttmockRegexMock.decorate
    def test_regex_url(self):
        response = requests.get('http://www.example.com/test')
        self.assertEqual(response.json(), HttmockCatchAllMock.item)
        response = requests.get('http://www.example.com')
        self.assertEqual(response.json(), HttmockCatchAllMock.item)
        response = requests.get('http://www.example.com/items/alpha/')
        self.assertEqual(response.json(), HttmockCatchAllMock.item)

        response = requests.get('http://www.example.com/items/1/')
        self.assertEqual(response.json(), HttmockRegexMock.item)
        response = requests.get('https://www.example.com/items/2/')
        self.assertEqual(response.json(), HttmockRegexMock.item)

###############################
# Regex for httpretty backend #
###############################


class HttprettyCatchAllMock(utils.BasePlacebo):
    item = {'all': True}
    url = (re.compile('.*') if utils.is_httpretty else '')
    body = json.dumps(item)


class HttprettyRegexMock(utils.BasePlacebo):
    item = {'name': 'Huseyin', 'last_name': 'Yilmaz'}
    url = (re.compile('^http(s)?://www.example.com/items/\d+/$')
           if utils.is_httpretty else '')
    body = json.dumps(item)


@unittest.skipUnless(utils.is_httpretty,
                     "Httpretty specific regex tests")
class HttprettyRegexTestCase(unittest.TestCase):
    """Httpretty specific tests"""
    # Because of how httpretty works order of decorators
    # Does not decide the priority. So if multiple decorators
    # match with with current url, one decorator will be choosen
    # randomly and used in response. For that reason we cannot
    # use HttprettyCatchAllMock. Instead we will match all urls
    # used in test separately. That way we will not have a url
    # that matches multiple mocks.
    # @HttprettyCatchAllMock.decorate
    @HttprettyCatchAllMock.decorate(url='http://www.example.com/test')
    @HttprettyCatchAllMock.decorate(url='http://www.example.com')
    @HttprettyCatchAllMock.decorate(url='http://www.example.com/items/alpha/')
    @HttprettyRegexMock.decorate
    def test_regex_url(self):
        # Urls that does not match with regex
        response = requests.get('http://www.example.com/test')
        self.assertEqual(response.json(), HttprettyCatchAllMock.item)
        response = requests.get('http://www.example.com')
        self.assertEqual(response.json(), HttprettyCatchAllMock.item)
        response = requests.get('http://www.example.com/items/alpha/')
        self.assertEqual(response.json(), HttprettyCatchAllMock.item)
        # Urls that matches regex
        response = requests.get('http://www.example.com/items/1/')
        self.assertEqual(response.json(), HttprettyRegexMock.item)
        response = requests.get('https://www.example.com/items/2/')
        self.assertEqual(response.json(), HttprettyRegexMock.item)
