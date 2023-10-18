def wildcard(prev, pattern, *args, **kw):
    """wildcard pipe greps data passed from previous generator
    according to given regular expression.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param pattern: The wildcard string which used to filter data.
    :type pattern: str|unicode|re pattern object
    :param inv: If true, invert the match condition.
    :type inv: boolean
    :returns: generator
    """
    import fnmatch

    inv = 'inv' in kw and kw.pop('inv')
    pattern_obj = re.compile(fnmatch.translate(pattern), *args, **kw)

    if not inv:
        for data in prev:
            if pattern_obj.match(data):
                yield data
    else:
        for data in prev:
            if not pattern_obj.match(data):
                yield data