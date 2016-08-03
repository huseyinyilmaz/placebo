from functools import partial
from functools import wraps
import urlparse

import six

from placebo import backends
from placebo.utils.datautils import invoke_or_get


class PlaceboData(object):
    """Class that represents request data for Placebo.

    This will be base class for placebo objects."""
    # Url that will be mocked
    url = NotImplemented
    body = NotImplemented
    headers = NotImplemented
    # Http method can be ('POST', 'GET', 'PUT', 'DELETE' etc.) default is 'GET'
    method = 'GET'
    # Http status code for response default is 200
    status = 200
    # Backend method for this instance
    backend = None

    def __init__(self,
                 f=None,
                 url=None,
                 body=None,
                 headers=None,
                 method=None,
                 status=None,
                 backend=None):
        """Initializer for placebo objects.

        Initializer will not be used directly. Placebo instances will be
        created by Placebo.decorate class method for each decorator.
        """
        # Value 'f' is not used. Placebo instances do not keep track of
        # functions being decorated. The reason f is in arguments is because
        # if it is provided that means Somebody is trying to use placebo
        # class as decorator. In that case we want to show an informative
        # error.
        if f is not None:
            raise ValueError(
                'Placebo object is not a decorator itself. '
                'Please use @Placebo.decorate instead of @Placebo')
        if url is not None:
            self.url = url
        if body is not None:
            self.body = body
        if headers is not None:
            self.headers = headers
        if method is not None:
            self.method = method
        if status is not None:
            self.status = status
        if backend is not None:
            self.backend = backend

    def _get_body(self, url, headers, body):
        if self.body is NotImplemented:
            raise NotImplementedError('To use placebo, you need to either '
                                      'provide body attribute or '
                                      'overwrite get_body method in subclass.')
        else:
            return invoke_or_get(self.body, url, headers, body)

    def _get_headers(self, url, headers, body):
        headers = self.headers
        if headers is NotImplemented:
            headers = {}
        return invoke_or_get(headers, url, headers, body)

    def _get_url(self):
        if self.url is NotImplemented:
            raise NotImplementedError('To use placebo, you need to either '
                                      'provide url attribute or '
                                      'overwrite get_url method in subclass.')
        else:
            url = invoke_or_get(self.url)
            # if url is a string convert it to ParsedUrl
            if isinstance(url, six.string_types):
                url = urlparse.urlparse(url)
            return url

    def _get_method(self):
        method = invoke_or_get(self.method)
        if not isinstance(method, six.string_types):
            raise ValueError('Method must be a string value.'
                             'Instead type %s provided. (%s)' %
                             (type(method), method))
        return method.upper()

    def _get_status(self):
        return invoke_or_get(self.status)

    @classmethod
    def get_backend(cls):
        """If backend is provided on child,
        use that backend. if it is not provided,
        go over all backends to find one that can be used.
        """
        if cls.backend is None:
            backend = backends.get_backend()
        else:
            # we cannot use invoke_or_get for
            # backend because backend is basicaly a function.
            backend = cls.backend
        return backend


class Placebo(PlaceboData):
    """Base class for placebo mocks."""

    @classmethod
    def mock(cls, f, **kwargs):
        """Actual mock method."""
        # create a placebo instance for backend
        placebo = cls(**kwargs)
        # choose a backend
        backend = cls.get_backend()
        # ask backend for decorator for current placebo instance.
        decorator = backend(placebo)
        # wrap decorator around curent function.
        return wraps(f)(decorator(f))

    @classmethod
    def decorate(cls, *args, **kwargs):
        """Utility to use mock as decorator and decorator with args.

        If mock has only one argument and no kwargs, we use mock as
        decorator directly, otherwise we use it decorator with kwargs."""
        if not args and kwargs:
            result = partial(cls.mock, **kwargs)
        else:
            result = cls.mock(*args, **kwargs)
        return result
