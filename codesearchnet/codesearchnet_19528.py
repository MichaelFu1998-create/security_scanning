def threaded(f, *args, **kwargs):
    """function decorator
    """
    if args or kwargs:
        return Threaded(f, *args, **kwargs)

    @wraps(f)
    def wrapped(*wargs, **wkwargs):
        return Threaded(f, *wargs, **wkwargs)

    return wrapped