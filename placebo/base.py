import urlparse
from placebo import backends


class Placebo(object):
    """Base class for placebo mocks."""

    # Url that will be mocked
    url = NotImplemented

    body = NotImplemented
    # Http method can be ('POST', 'GET', 'PUT', 'DELETE' etc.) default is 'GET'
    method = 'GET'
    # Http status code for response default is 200
    status = 200

    def get_body(self, url, request):
        if self.body is NotImplemented:
            raise NotImplementedError('To use placebo, you need to either '
                                      'provide body attribute or '
                                      'overwrite get_body method in subclass.')
        else:
            return self.body

    def get_url(self):
        if self.body is NotImplemented:
            raise NotImplementedError('To use placebo, you need to either '
                                      'provide url attribute or '
                                      'overwrite get_url method in subclass.')
        else:
            return urlparse.urlparse(self.url)

    def mock(self, f):
        backend_class = backends.get_backend()
        backend = backend_class(placebo=self)
        decorator = backend.get_decorator()
        return decorator(f)
