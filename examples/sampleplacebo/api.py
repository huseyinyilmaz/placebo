import unittest
import json
import requests
from placebo import Placebo

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
        api = ItemAPIClient()
        with self.assertRaises(ItemException):
            api.get_items()

    @SimplePlaceboWithAllFields.decorate
    def test_valid_list_valid_full(self):
        api = ItemAPIClient()
        result = api.get_items()
        self.assertEqual(result,
                         [{"id": 1}, {"id": 2}, {"id": 3}])


if __name__ == '__main__':
    unittest.main()
