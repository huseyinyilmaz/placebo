import six
from six.moves.urllib import parse


class PlaceboRequest(object):
    """Utility class targeted to make inspecting requests easier."""
    # Main Data Attributes
    # Values will be filled in initializer.
    url = None
    parsed_url = None
    headers = None
    body = None

    def __init__(self, url, headers, body):
        if isinstance(url, (parse.ParseResult, parse.SplitResult)):
            self.url = url.geturl()
            self.parsed_url = url
        elif isinstance(url, six.string_types):
            self.url = url
            self.parsed_url = parse.urlparse(url)

        self.headers = headers
        self.body = body

    def __str__(self):
        return '<PlaceboRequest %s>' % self.url

    def __repr__(self):
        return 'PlaceboRequest(%s, %s, %s)' % (self.url,
                                               self.headers,
                                               self.data)

    @property
    def query(self):
        return parse.parse_qs(self.parsed_url.query,
                              keep_blank_values=True)
