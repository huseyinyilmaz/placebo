import logging
from six.moves.urllib import parse

import httpretty

logger = logging.getLogger(__name__)

HEADER_WARNING = ('Placebo warning: Please beware that httppretty has known '
                  'problems when you use multiple Placebo mocks that updates '
                  'headers. If you have any problems with mixing headers, '
                  'please consider chaning your backend to httmockbackend or '
                  'do not stack such Placebo mocks on top of each other.')


def get_decorator(placebo):
    """Create a decorator for placebo object."""
    def decorator(fun):
        def _wrapper(*args, **kwargs):
            def _run():
                method = placebo._get_method()

                def get_body(request, uri, headers):
                    url = parse.urlparse(uri)
                    response_headers = placebo._get_headers(url,
                                                            headers,
                                                            request.body)
                    if response_headers:
                        logger.warn(HEADER_WARNING)

                    response_body = placebo._get_body(url,
                                                      headers,
                                                      request.body)
                    return (placebo.status, response_headers, response_body)
                    # return response.status, response.headers, response.data
                httpretty.register_uri(getattr(httpretty, method),
                                       placebo._get_url().geturl(),
                                       body=get_body)
                response = fun(*args, **kwargs)
                return response

            # run-time check if httppretty is enabled.
            # We must enable httpretty only once.
            # This is necessary to chain
            # multiple mock objects together.
            if not httpretty.is_enabled():
                _run = httpretty.activate(_run)
            return _run()
        return _wrapper
    return decorator
