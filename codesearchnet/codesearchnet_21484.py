def cache_func(prefix, method=False):
    """
    Cache result of function execution into the django cache backend.
    Calculate cache key based on `prefix`, `args` and `kwargs` of the function.
    For using like object method set `method=True`.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_args = args
            if method:
                cache_args = args[1:]
            cache_key = get_cache_key(prefix, *cache_args, **kwargs)
            cached_value = cache.get(cache_key)
            if cached_value is None:
                cached_value = func(*args, **kwargs)
                cache.set(cache_key, cached_value)
            return cached_value
        return wrapper
    return decorator