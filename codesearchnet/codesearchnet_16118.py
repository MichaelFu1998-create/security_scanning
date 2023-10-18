def search_pattern(regex):
    """
    Return a value check function which raises a ValueError if the supplied
    regular expression does not match anywhere in the value, see also
    `re.search`.

    """

    prog = re.compile(regex)
    def checker(v):
        result = prog.search(v)
        if result is None:
            raise ValueError(v)
    return checker