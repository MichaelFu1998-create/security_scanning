def argflag(key, argv=None):
    """
    Determines if a key is specified on the command line

    Args:
        key (str or tuple): string or tuple of strings. Each key should be
            prefixed with two hyphens (i.e. `--`)
        argv (Optional[list]): overrides `sys.argv` if specified

    Returns:
        bool: flag : True if the key (or any of the keys) was specified

    Example:
        >>> import ubelt as ub
        >>> argv = ['--spam', '--eggs', 'foo']
        >>> assert ub.argflag('--eggs', argv=argv) is True
        >>> assert ub.argflag('--ans', argv=argv) is False
        >>> assert ub.argflag('foo', argv=argv) is True
        >>> assert ub.argflag(('bar', '--spam'), argv=argv) is True
    """
    if argv is None:  # nocover
        argv = sys.argv
    keys = [key] if isinstance(key, six.string_types) else key
    flag = any(k in argv for k in keys)
    return flag