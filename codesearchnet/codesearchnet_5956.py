def gcp_stats():
    """
    Collect stats

    Specifically, time function calls
    :returns: function response
    :rtype: varies
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            result = f(*args, **kwargs)
            end_time = time.time()
            strkey = _build_key(f.__name__, args, kwargs)
            _GCP_STATS.setdefault(strkey, []).append(end_time - start_time)
            return result

        return decorated_function

    return decorator