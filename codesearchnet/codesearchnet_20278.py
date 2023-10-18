def api_call_action(func): 
    """
    API wrapper documentation
    """
    def _inner(*args, **kwargs):
        return func(*args, **kwargs)
    _inner.__name__ = func.__name__
    _inner.__doc__ = func.__doc__
    return _inner