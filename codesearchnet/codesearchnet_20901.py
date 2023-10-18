def build_call_str(prefix, args, kwargs):
    # type: (str, Any, Any) -> str
    '''
    Build a callable Python string for a function call. The output will be
    combined similar to this template::

        <prefix>(<args>, <kwargs>)

    Example::

        >>> build_call_str('foo', (1, 2), {'a': '10'})
        "foo(1, 2, a='10')"
    '''
    kwargs_str = ', '.join(['%s=%r' % (key, value) for key, value in
                            kwargs.items()])
    args_str = ', '.join([repr(arg) for arg in args])
    output = [prefix, '(']
    if args:
        output.append(args_str)
    if args and kwargs:
        output.append(', ')
    if kwargs:
        output.append(kwargs_str)
    output.append(')')
    return ''.join(output)