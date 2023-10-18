def cache_result(func):
    """
    Decorator to cache the result of functions that take a ``user`` and a
    ``size`` value.
    """
    def cache_set(key, value):
        cache.set(key, value, AVATAR_CACHE_TIMEOUT)
        return value

    def cached_func(user, size):
        prefix = func.__name__
        cached_funcs.add(prefix)
        key = get_cache_key(user, size, prefix=prefix)
        return cache.get(key) or cache_set(key, func(user, size))
    return cached_func