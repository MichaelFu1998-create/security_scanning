def indexesOptional(f):
    """Decorate test methods with this if you don't require strict index checking"""
    stack = inspect.stack()
    _NO_INDEX_CHECK_NEEDED.add('%s.%s.%s' % (f.__module__, stack[1][3], f.__name__))
    del stack
    return f