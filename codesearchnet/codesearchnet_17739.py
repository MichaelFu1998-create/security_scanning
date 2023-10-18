def xformers(sig):
    """
    Get the list of xformer functions for the given signature.

    :param str sig: a signature
    :returns: a list of xformer functions for the given signature.
    :rtype: list of tuple of a function * str

    Each function catches all TypeErrors it encounters and raises
    corresponding IntoDPValueError exceptions.
    """
    return \
       [(_wrapper(f), l) for (f, l) in \
       _XFORMER.PARSER.parseString(sig, parseAll=True)]