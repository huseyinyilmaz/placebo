"""Tests for main httppretty."""

from tests.basetestcase import BaseTestCase
from placebo.backends.httprettybackend import get_decorator


class HttprettyTestCase(BaseTestCase):
    """Httpretty tests."""


# monkey patch mock class
HttprettyTestCase.GetMock._resolve_backend = lambda: get_decorator
