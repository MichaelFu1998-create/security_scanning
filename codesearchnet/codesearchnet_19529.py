def spawn(f, *args, **kwargs):
    """decorator
    """
    if args or kwargs:
        return Spawn(f, *args, **kwargs)

    @wraps(f)
    def wrapped(*args, **kwargs):
        return Spawn(f, *args, **kwargs)

    return wrapped