def depricated_name(newmethod):
    """
    Decorator for warning user of depricated functions before use.

    Args:
        newmethod (str): Name of method to use instead.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning) 
            warnings.warn(
                "Function {} is depricated, please use {} instead.".format(func.__name__, newmethod),
                category=DeprecationWarning, stacklevel=2
            )
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)
        return wrapper
    return decorator