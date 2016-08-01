from placebo.backends.base import BaseBackend
import httmock


def get_decorator(placebo):
    url = placebo.get_url()

    @httmock.urlmatch(scheme=url.scheme,
                      netloc=url.netloc,
                      path=url.path,
                      method=placebo.method,
                      query=url.query)
    def mock_response(url, request):
        placebo._last_request = request
        return {'status': placebo.status,
                'content': placebo.get_body(url, request)}

    return httmock.with_httmock(mock_response)
