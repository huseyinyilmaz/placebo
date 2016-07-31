class BaseBackend(object):

    def __init__(self, placebo):
        self.placebo = placebo

    def is_supported(self):
        """Checks if current backend can be used with current depencencies."""
        raise NotImplementedError('is_supported must be overritten '
                                  'on backend classes.')

    def get_decorator(self):
        """Returns a decorator that can be wrapped around."""
        raise NotImplementedError('get_decorator must be overritten '
                                  'on backend classes.')
