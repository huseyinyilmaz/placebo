import os
from placebo import Placebo
from placebo.utils.importutils import import_string

httpretty_path = 'placebo.backends.httprettybackend.get_decorator'
httmock_path = 'placebo.backends.httmockbackend.get_decorator'
# Get value from environment.
backend_str = os.environ.get('PLACEBO_BACKEND', httmock_path)
# There are some some unexpected behaviors we get from httpretty
# so some tests must be disabled for httpretty
is_httpretty = (backend_str == httpretty_path)
is_httmock = (backend_str == httmock_path)

backend = import_string(backend_str)


class BasePlacebo(Placebo):
    backend = backend


def remove_common_headers(headers):
    common_headers = ['content-type', 'content-length']
    for header in common_headers:
        if header in headers:
            del headers[header]
    return headers
