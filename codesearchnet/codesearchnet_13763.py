def print_defaults():
    """Pretty-print the contents of :data:`DEFAULTS`"""
    maxlen = max([len(x) for x in DEFAULTS])
    for key in DEFAULTS:
        value = DEFAULTS[key]
        if isinstance(value, (list, set)):
            value = ', '.join(value)
        print "%*s: %s" % (maxlen, key, value)