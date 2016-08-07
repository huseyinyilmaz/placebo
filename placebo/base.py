from functools import partial
from functools import wraps
import six

from placebo import backends
from placebo.request import PlaceboRequest
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
        # we want to keep latest request to use do tests
        self._set_last_request(url, headers, body)
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
        """
        Returns: string_type or parse.ParseResult or parse SplitResult
        We have a vague return type for _get_url method
        because we could not generalise regex support for all
        backends. So we are directly passing result to backends.
        That way users can use regex that their backend provides.
        """
        if self.url is NotImplemented:
            raise NotImplementedError('To use placebo, you need to either '
                                      'provide url attribute or '
                                      'overwrite get_url method in subclass.')
        else:
            url = invoke_or_get(self.url)
            # if url is a string convert it to ParsedUrl
            # if isinstance(url, six.string_types):
            #     url = parse.urlparse(url)
            # TODO: check return type
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
    def _resolve_backend(cls):
        """Dependency injection hook."""
        return backends.get_backend()

    @classmethod
    def get_backend(cls):
        """If backend is provided on child,
        use that backend. if it is not provided,
        go over all backends to find one that can be used.
        """
        if cls.backend is None:
            backend = cls._resolve_backend()
        else:
            # we cannot use invoke_or_get for
            # backend because backend is basicaly a function.
            backend = cls.backend
        return backend

    @classmethod
    def _set_last_request_on_class(cls, request):
        cls.last_request = request

    def _set_last_request(self, url, headers, body):
        """Set last request on body to keep track of changes"""
        request = PlaceboRequest(url, headers, body)
        self._set_last_request_on_class(request)
        self.last_request = request


class Placebo(PlaceboData):
    """Base class for placebo mocks."""

    @classmethod
    def mock(cls, f, arg_name=None, **kwargs):
        """Actual mock method."""
        # create a placebo instance for backend
        placebo = cls(**kwargs)
        # choose a backend
        backend = cls.get_backend()
        # if arg_name is provided, add current
        # placebo instance to function's kwargs.
        if arg_name is not None:
            f = wraps(f)(partial(f, **{arg_name: placebo}))
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

    def __str__(self):
        return '<%s %s>' % (self.__class__.__name__, str(self.url))

    def __repr__(self):
        return str(self)
