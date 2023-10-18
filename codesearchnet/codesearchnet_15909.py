def format_docstring(*args, **kwargs):
    """
    Decorator for clean docstring formatting
    """
    def decorator(func):
        func.__doc__ = getdoc(func).format(*args, **kwargs)
        return func
    return decorator