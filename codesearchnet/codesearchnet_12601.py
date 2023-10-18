def operator(name=None, operators=None, aliases=None, kind=None):
    """
    Registers a new operator function in the test engine.

    Arguments:
        *args: variadic arguments.
        **kw: variadic keyword arguments.

    Returns:
        function
    """
    def delegator(assertion, subject, expected, *args, **kw):
        return assertion.test(subject, expected, *args, **kw)

    def decorator(fn):
        operator = Operator(fn=fn, aliases=aliases, kind=kind)
        _name = name if isinstance(name, six.string_types) else fn.__name__
        operator.operators = (_name,)

        _operators = operators
        if isinstance(_operators, list):
            _operators = tuple(_operators)

        if isinstance(_operators, tuple):
            operator.operators += _operators

        # Register operator
        Engine.register(operator)
        return functools.partial(delegator, operator)

    return decorator(name) if inspect.isfunction(name) else decorator