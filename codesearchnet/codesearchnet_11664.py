def sometimesPruneCache(p):
    ''' return decorator to prune cache after calling fn with a probability of p'''
    def decorator(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            r = fn(*args, **kwargs)
            if random.random() < p:
                pruneCache()
            return r
        return wrapped
    return decorator