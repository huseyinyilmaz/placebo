"""Tests for main httpmock."""
from tests.basetestcase import BaseTestCase
from placebo.backends.httmockbackend import get_decorator


class HttmockTestCase(BaseTestCase):
    """Httmock tests."""

# monkey patch mock class
HttmockTestCase.GetMock.backend = get_decorator
