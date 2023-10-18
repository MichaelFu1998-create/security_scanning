def docstring(docstr):
    """
    Decorates a function with the given docstring

    Parameters
    ----------
    docstr : string
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__doc__ = docstr
        return wrapper
    return decorator