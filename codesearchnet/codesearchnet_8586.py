def ignore_warning(warning):
    """
    Ignore any emitted warnings from a function.

    :param warning: The category of warning to ignore.
    """
    def decorator(func):
        """
        Return a decorated function whose emitted warnings are ignored.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrap the function.
            """
            warnings.simplefilter('ignore', warning)
            return func(*args, **kwargs)
        return wrapper
    return decorator