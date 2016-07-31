from operator import methodcaller
from placebo.backends import httmockbackend

default_backends = [
    httmockbackend.Backend
]


def get_backend():
    """Returns a backend that has correct dependencies."""
    backend = next(filter(methodcaller('is_supported'), default_backends),
                   None)
    if backend is None:
        raise ValueError('No backend is supported. (Did you install any of'
                         'mock dependencies like httmock or httpretty?)')
    else:
        return backend
