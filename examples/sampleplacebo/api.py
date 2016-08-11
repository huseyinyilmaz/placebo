import unittest
import json
import requests
from placebo import Placebo
import re
from six.moves.urllib import parse
import six

######################
# API client to test #
######################


class ItemException(Exception):
    """Sample Exception class to raise."""


class ItemAPIClient:
    """Sample Item API Client"""

    list_url = 'http://www.acme.com/items/'
    item_url = 'http://www.acme.com/items/%s/'

    def get_items(self):
        """Gets list of sample items."""
        response = requests.get(self.list_url)
        if not response.ok:
            raise ItemException('List API returned an error')
        else:
            return response.json()

    def get_item(self, item_id):
        url = self.item_url % item_id
        response = requests.get(url)
        if not response.ok:
            raise ItemException('List API returned an error')
        else:
            return response.json()

###################
# PLACEBO OBJECTS #
###################


class SimplePlacebo(Placebo):
    url = 'http://www.acme.com/items/'
    body = '[{"id": 1}, {"id": 2}, {"id": 3}]'


class SimplePlaceboWithAllFields(Placebo):
    url = 'http://www.acme.com/items/'
    body = '[{"id": 1}, {"id": 2}, {"id": 3}]'
    status = 200
    method = 'GET'
    headers = {'custom-header': 'custom'}


class DynamicPlacebo(Placebo):
    url_regex = re.compile('^http://www.acme.com/items/(?P<item_id>\d+)/$')

    def url(self):
        return parse.ParseResult(
            scheme='http',
            netloc=r'www\.acme\.com',
            path=r'^/items/(\d+)/$',
            params='',
            query='',
            fragment='')

    def method(self):
        return 'GET'

    def body(self, request_url, request_headers, request_body):
        url = request_url.geturl()
        item_id = self.url_regex.match(url).groupdict()['item_id']
        return json.dumps({'id': int(item_id)})

    def headers(self, request_url, request_headers, request_body):
        return {}

    def status(self, request_url, request_headers, request_body):
        return 200


#############
# UNITTESTS #
#############

class SimpleTestCase(unittest.TestCase):

    @SimplePlacebo.decorate
    def test_get_list_valid(self):
        api = ItemAPIClient()
        result = api.get_items()
        self.assertEqual(result,
                         [{"id": 1}, {"id": 2}, {"id": 3}])

    @SimplePlacebo.decorate(status=500)
    def test_get_list_error(self):
        api = ItemAPIClient()
        with self.assertRaises(ItemException):
            api.get_items()

    @SimplePlacebo.decorate(body='invalid-body')
    def test_get_list_invalid_body_error(self):
        "This test does not pass. Feel free to fix it and open a pr :)"
        api = ItemAPIClient()
        with self.assertRaises(ItemException):
            api.get_items()

    @SimplePlaceboWithAllFields.decorate
    def test_valid_list_valid_full(self):
        api = ItemAPIClient()
        result = api.get_items()
        self.assertEqual(result,
                         [{"id": 1}, {"id": 2}, {"id": 3}])


class DynamicPlaceboTestCase(unittest.TestCase):


    @DynamicPlacebo.decorate
    def test_get_item_valid(self):
        api = ItemAPIClient()
        # id = 1
        resp = api.get_item(1)
        self.assertEqual(resp, {'id': 1})
        # id = 2
        resp = api.get_item(2)
        self.assertEqual(resp, {'id': 2})


if __name__ == '__main__':
    unittest.main()
