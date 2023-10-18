def fnmatches(fname, patterns, matchfun):
    """"
    matches?
    :param fname: file name
    :type fname: str
    :param patterns: list of filename pattern. see fnmatch.fnamtch
    :type patterns: [str]
    :rtype: generator of bool
    """
    import fnmatch
    matchfun = matchfun or fnmatch.fnmatch
    for p in patterns:
        yield matchfun(fname, p)