"""Data conversation related functions."""


def extract_function(f, *args, **kwargs):
    """if f is callable it calls f with given args and kwargs and return the
       value. If f is not callable return f directly.
    """
    if callable(f):
        return f(*args, **kwargs)
    else:
        return f
