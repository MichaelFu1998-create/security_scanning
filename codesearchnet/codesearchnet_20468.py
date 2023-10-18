def iteritems(data, **kwargs):
    """Iterate over dict items."""
    return iter(data.items(**kwargs)) if IS_PY3 else data.iteritems(**kwargs)