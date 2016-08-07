from six.moves.urllib import parse
import six
import httmock


def get_decorator(placebo):
    url = placebo._get_url()

    if isinstance(url, six.string_types):
        url = parse.urlparse(url)

    # TODO should we remove empty parts of url?
    match_kwargs = {
        'scheme': url.scheme,
        'netloc': url.netloc,
        'path': url.path,
        'method': placebo._get_method(),
        'query': url.query
    }

    match_kwargs = {k: v
                    for k, v in match_kwargs.items()
                    if v}

    @httmock.urlmatch(**match_kwargs)
    def mock_response(url, request):
        # Convert parse result type from SplitResult to ParseResult
        url = parse.urlparse(url.geturl())
        # if body is empty httmock returns None
        # but we want ot to be always string.
        body = request.body or ''
        headers = request.headers
        return {'status_code': placebo._get_status(),
                'content': placebo._get_body(url, headers, body),
                'headers': placebo._get_headers(url, headers, body)}

    return httmock.with_httmock(mock_response)
