def attribute(*args, **kw):
    """
    Registers a new attribute only operator function in the test engine.

    Arguments:
        *args: variadic arguments.
        **kw: variadic keyword arguments.

    Returns:
        function
    """
    return operator(kind=Operator.Type.ATTRIBUTE, *args, **kw)