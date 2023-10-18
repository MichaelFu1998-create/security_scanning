def signature_matches(func, args=(), kwargs={}):
    """
    Work out if a function is callable with some args or not.
    """
    try:
        sig = inspect.signature(func)
        sig.bind(*args, **kwargs)
    except TypeError:
        return False
    else:
        return True