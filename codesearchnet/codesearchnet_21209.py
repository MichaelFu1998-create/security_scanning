def keywords(func):
    """
    Accumulate all dictionary and named arguments as
    keyword argument dictionary. This is generally useful for
    functions that try to automatically resolve inputs.

    Examples:
        >>> @keywords
        >>> def test(*args, **kwargs):
        >>>     return kwargs
        >>>
        >>> print test({'one': 1}, two=2)
        {'one': 1, 'two': 2}
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        idx = 0 if inspect.ismethod(func) else 1
        if len(args) > idx:
            if isinstance(args[idx], (dict, composite)):
                for key in args[idx]:
                    kwargs[key] = args[idx][key]
                args = args[:idx]
        return func(*args, **kwargs)
    return decorator