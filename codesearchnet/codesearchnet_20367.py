def parse_directive(key):
    """
    Takes a key of type (foo:bar) and returns either the key and the
    directive, or the key and None (for no directive.)
    """
    if constants.DIRECTIVE in key:
        return key.split(constants.DIRECTIVE, 1)
    else:
        return key, None