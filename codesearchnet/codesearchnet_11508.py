def kwarg_decorator(func):
    """
    Turns a function that accepts a single arg and some kwargs in to a
    decorator that can optionally be called with kwargs:

    .. code-block:: python

        @kwarg_decorator
        def my_decorator(func, bar=True, baz=None):
            ...

        @my_decorator
        def my_func():
            pass

        @my_decorator(bar=False)
        def my_other_func():
            pass
    """
    @wraps(func)
    def decorator(arg=None, **kwargs):
        if arg is None:
            return lambda arg: decorator(arg, **kwargs)
        return func(arg, **kwargs)
    return decorator