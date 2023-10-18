def multiglob_compile(globs, prefix=False):
    """Generate a single "A or B or C" regex from a list of shell globs.

    :param globs: Patterns to be processed by :mod:`fnmatch`.
    :type globs: iterable of :class:`~__builtins__.str`

    :param prefix: If ``True``, then :meth:`~re.RegexObject.match` will
        perform prefix matching rather than exact string matching.
    :type prefix: :class:`~__builtins__.bool`

    :rtype: :class:`re.RegexObject`
    """
    if not globs:
        # An empty globs list should only match empty strings
        return re.compile('^$')
    elif prefix:
        globs = [x + '*' for x in globs]
    return re.compile('|'.join(fnmatch.translate(x) for x in globs))