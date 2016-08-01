import logging

from placebo.utils.importutils import import_string

logger = logging.getLogger(__name__)


default_backends = [
    'placebo.backends.httmockbackend.get_decorator',
    'placebo.backends.httprettybackend.get_decorator',
]


def get_backend():
    """Returns a backend that has correct dependencies."""

    # try to import backends one by one.
    backend = None
    for st in default_backends:
        try:
            backend = import_string(st)
            break
        except ImportError as e:
            logger.warning('Could not import %s: %s', st, e)

    if backend is None:
        raise ValueError('No backend is supported. (Did you install any of'
                         'mock dependencies like httmock or httpretty?)')
    else:
        return backend
