def gcp_cache(future_expiration_minutes=15):
    """
    Cache function output
    :param future_expiration_minutes: Number of minutes in the future until item
                                      expires.  Default is 15.
    :returns: function response, optionally from the cache
    :rtype: varies
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            strkey = _build_key(f.__name__, args, kwargs)
            cached_result = _GCP_CACHE.get(strkey)
            if cached_result:
                return cached_result
            else:
                result = f(*args, **kwargs)
                _GCP_CACHE.insert(strkey, result, future_expiration_minutes)
            return result

        return decorated_function

    return decorator