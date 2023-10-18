def match_pattern(regex):
    """
    Return a value check function which raises a ValueError if the value does
    not match the supplied regular expression, see also `re.match`.

    """

    prog = re.compile(regex)
    def checker(v):
        result = prog.match(v)
        if result is None:
            raise ValueError(v)
    return checker