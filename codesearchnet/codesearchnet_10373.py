def hasmethod(obj, m):
    """Return ``True`` if object *obj* contains the method *m*.

    .. versionadded:: 0.7.1
    """
    return hasattr(obj, m) and callable(getattr(obj, m))