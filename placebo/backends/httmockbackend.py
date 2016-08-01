import urlparse

import httmock


def get_decorator(placebo):
    url = placebo.get_url()

    @httmock.urlmatch(scheme=url.scheme,
                      netloc=url.netloc,
                      path=url.path,
                      method=placebo.get_method(),
                      query=url.query)
    def mock_response(url, request):
        # Convert parse result type from SplitResult to ParseResult
        url = urlparse.urlparse(url.geturl())
        # if body is empty httmock returns None
        # but we want ot to be always string.
        body = request.body or ''
        headers = request.headers
        placebo._last_request = request
        return {'status': placebo.status,
                'content': placebo.get_body(url, headers, body)}

    return httmock.with_httmock(mock_response)
