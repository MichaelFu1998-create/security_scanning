def _invalidates_cache(f):
    """
    Decorator for rruleset methods which may invalidate the
    cached length.
    """

    def inner_func(self, *args, **kwargs):
        rv = f(self, *args, **kwargs)
        self._invalidate_cache()
        return rv

    return inner_func