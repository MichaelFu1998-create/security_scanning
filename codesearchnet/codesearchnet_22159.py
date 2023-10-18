def _normalize_instancemethod(instance_method):
    """
    wraps(instancemethod) returns a function, not an instancemethod so its repr() is all messed up;
    we want the original repr to show up in the logs, therefore we do this trick
    """
    if not hasattr(instance_method, 'im_self'):
        return instance_method

    def _func(*args, **kwargs):
        return instance_method(*args, **kwargs)

    _func.__name__ = repr(instance_method)
    return _func