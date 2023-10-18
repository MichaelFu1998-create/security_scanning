def deprecated(extra):
    """
    Flag a method as deprecated.

    :param extra: Extra text you'd like to display after the default text.
    """
    def decorator(func):
        """
        Return a decorated function that emits a deprecation warning on use.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrap the function.
            """
            message = 'You called the deprecated function `{function}`. {extra}'.format(
                function=func.__name__,
                extra=extra
            )
            frame = inspect.currentframe().f_back
            warnings.warn_explicit(
                message,
                category=DeprecationWarning,
                filename=inspect.getfile(frame.f_code),
                lineno=frame.f_lineno
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator