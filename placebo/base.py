import urlparse
from functools import wraps

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

    backend = None

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

    @classmethod
    def get_backend(cls):
        """If backend is provided on child,
        use that backend. if it is not provided,
        go over all backends to find one that can be used.
        """
        if cls.backend is None:
            backend = backends.get_backend()
        else:
            backend = cls.backend
        return backend

    @classmethod
    def mock(cls, f):
        placebo = cls()
        backend = cls.get_backend()
        decorator = backend(placebo)
        return wraps(f)(decorator(f))
