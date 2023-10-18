def cache_method(func=None, prefix=''):
    """
    Cache result of function execution into the `self` object (mostly useful in models).
    Calculate cache key based on `args` and `kwargs` of the function (except `self`).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key_prefix = prefix or '_cache_{}'.format(func.__name__)
            cache_key = get_cache_key(cache_key_prefix, *args, **kwargs)
            if not hasattr(self, cache_key):
                setattr(self, cache_key, func(self))
            return getattr(self, cache_key)
        return wrapper
    if func is None:
        return decorator
    else:
        return decorator(func)