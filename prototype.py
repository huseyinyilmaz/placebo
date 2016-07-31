"""File that I will be doing some prototyping. It will be removed later."""

import json


class BaseMock():
    def get_body(self, url, request):
        pass

    def get_url(self, url, request):
        pass


class Response(BaseMock):

    url = 'http://www.acme.com/api/v1/users/'
    body = json.dumps([{'name': 'Huseyin',
                        'last_name': 'Yilmaz'}])

    method = 'GET'

    def get_body(self, url, request):
        """"""
        # TODO: should we convert the request we have here to a
        # generic request?
        return json.dumps([{'name': 'Huseyin',
                            'last_name': 'Yilmaz'}])

    def get_url(self):
        """"""
        return json.dumps([{'name': 'Huseyin',
                            'last_name': 'Yilmaz'}])
