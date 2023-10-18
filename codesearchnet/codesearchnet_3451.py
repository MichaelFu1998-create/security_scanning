def deprecated(message: str):
    """A decorator for marking functions as deprecated. """
    assert isinstance(message, str), "The deprecated decorator requires a message string argument."

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(f"`{func.__qualname__}` is deprecated. {message}",
                          category=ManticoreDeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator