def argval(key, default=util_const.NoParam, argv=None):
    """
    Get the value of a keyword argument specified on the command line.

    Values can be specified as `<key> <value>` or `<key>=<value>`

    Args:
        key (str or tuple): string or tuple of strings. Each key should be
            prefixed with two hyphens (i.e. `--`)
        default (Optional[object]): value to return if not specified
        argv (Optional[list]): overrides `sys.argv` if specified

    Returns:
        str: value : the value specified after the key. It they key is
            specified multiple times, then the first value is returned.

    TODO:
        - [ ] Can we handle the case where the value is a list of long paths?
        - [ ] Should we default the first or last specified instance of the flag.

    Example:
        >>> import ubelt as ub
        >>> argv = ['--ans', '42', '--quest=the grail', '--ans=6', '--bad']
        >>> assert ub.argval('--spam', argv=argv) == ub.NoParam
        >>> assert ub.argval('--quest', argv=argv) == 'the grail'
        >>> assert ub.argval('--ans', argv=argv) == '42'
        >>> assert ub.argval('--bad', argv=argv) == ub.NoParam
        >>> assert ub.argval(('--bad', '--bar'), argv=argv) == ub.NoParam

    Example:
        >>> # Test fix for GH Issue #41
        >>> import ubelt as ub
        >>> argv = ['--path=/path/with/k=3']
        >>> ub.argval('--path', argv=argv) == '/path/with/k=3'
    """
    if argv is None:  # nocover
        argv = sys.argv

    keys = [key] if isinstance(key, six.string_types) else key
    n_max = len(argv) - 1
    for argx, item in enumerate(argv):
        for key_ in keys:
            if item == key_:
                if argx < n_max:
                    value = argv[argx + 1]
                    return value
            elif item.startswith(key_ + '='):
                value = '='.join(item.split('=')[1:])
                return value
    value = default
    return value