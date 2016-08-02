import urlparse

import httpretty


def get_decorator(placebo):
    """Create a decorator for placebo object."""
    def decorator(fun):
        def _wrapper(*args, **kwargs):
            def _run():
                method = placebo.get_method()

                def get_body(request, uri, headers):
                    url = urlparse.urlparse(uri)
                    response_headers = placebo.get_headers(url,
                                                           headers,
                                                           request.body)
                    response_body = placebo.get_body(url,
                                                     headers,
                                                     request.body)
                    return (placebo.status, response_headers, response_body)
                    # return response.status, response.headers, response.data
                httpretty.register_uri(getattr(httpretty, method),
                                       placebo.get_url().geturl(),
                                       body=get_body)
                # status=placebo.status,)

                response = fun(*args, **kwargs)
                return response

            # run-time check if httppretty is enabled.
            # We need to enable httpretty only once.
            # This is necessary to chain
            # multiple mock objects together.
            if not httpretty.is_enabled():
                _run = httpretty.activate(_run)

            return _run()
        return _wrapper
    return decorator
