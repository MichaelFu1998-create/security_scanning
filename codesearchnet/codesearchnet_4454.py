def interactive(f):
    """Decorator for making functions appear as interactively defined.

    This results in the function being linked to the user_ns as globals()
    instead of the module globals().
    """
    # build new FunctionType, so it can have the right globals
    # interactive functions never have closures, that's kind of the point
    if isinstance(f, FunctionType):
        mainmod = __import__('__main__')
        f = FunctionType(f.__code__, mainmod.__dict__,
                         f.__name__, f.__defaults__,
                         )
    # associate with __main__ for uncanning
    f.__module__ = '__main__'
    return f