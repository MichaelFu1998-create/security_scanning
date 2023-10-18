def besttype(x):
    """Convert string x to the most useful type, i.e. int, float or unicode string.

    If x is a quoted string (single or double quotes) then the quotes
    are stripped and the enclosed string returned.

    .. Note::

       Strings will be returned as Unicode strings (using :func:`to_unicode`).

    .. versionchanged:: 0.7.0
       removed `encoding keyword argument
    """
    x = to_unicode(x)  # make unicode as soon as possible
    try:
        x = x.strip()
    except AttributeError:
        pass
    m = re.match(r"""['"](?P<value>.*)["']$""", x)
    if m is None:
        # not a quoted string, try different types
        for converter in int, float, to_unicode:   # try them in increasing order of lenience
            try:
                return converter(x)
            except ValueError:
                pass
    else:
        # quoted string
        x = to_unicode(m.group('value'))
    return x