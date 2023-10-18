def iterkeys(data, **kwargs):
    """Iterate over dict keys."""
    return iter(data.keys(**kwargs)) if IS_PY3 else data.iterkeys(**kwargs)