def decorator(decorator_func):
    """Allows a decorator to be called with or without keyword arguments."""
    assert callable(decorator_func), type(decorator_func)

    def _decorator(func=None, **kwargs):
        assert func is None or callable(func), type(func)
        if func:
            return decorator_func(func, **kwargs)
        else:
            def _decorator_helper(func):
                return decorator_func(func, **kwargs)

            return _decorator_helper

    return _decorator