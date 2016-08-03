"""Data conversation related functions."""


def invoke_or_get(f, *args, **kwargs):
    """if f is callable this function invoke f with given args and kwargs
    and return the value. If f is not callable return f directly.
    """
    if callable(f):
        return f(*args, **kwargs)
    else:
        return f
