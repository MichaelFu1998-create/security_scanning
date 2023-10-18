def maybe(f, default=None):
    """
    Create a nil-safe callable decorator.

    If the wrapped callable receives ``None`` as its argument, it will return
    ``None`` immediately.
    """
    @wraps(f)
    def _maybe(x, *a, **kw):
        if x is None:
            return default
        return f(x, *a, **kw)
    return _maybe