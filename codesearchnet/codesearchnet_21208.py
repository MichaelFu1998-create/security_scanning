def exception(exception):
    """
    Wrap function/method with specific exception if any
    exception occurs during function execution.
 
    Args:
        exception (Exception): Exception to re-cast error as.

    Examples:
        >>> from gems import exception
        >>>
        >>> class MyCustomException(Exception):
        >>>     pass
        >>>
        >>> @exception(MyCustomException)
        >>> def func():
        >>>     return 1 / 0
        >>>
        >>> func()
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "gems/decorators.py", line 96, in wrapper
            return func(*args, **kwargs)
          File "<stdin>", line 3, in func
        __main__.MyCustomException: integer division or modulo by zero
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exe:
                raise raise_with_traceback(exception(exe))
        return wrapper
    return decorator