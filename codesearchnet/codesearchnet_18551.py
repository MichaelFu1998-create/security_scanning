def grep(prev, pattern, *args, **kw):
    """The pipe greps the data passed from previous generator according to
    given regular expression.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param pattern: The pattern which used to filter out data.
    :type pattern: str|unicode|re pattern object
    :param inv: If true, invert the match condition.
    :type inv: boolean
    :param kw:
    :type kw: dict
    :returns: generator
    """
    inv = False if 'inv' not in kw else kw.pop('inv')
    pattern_obj = re.compile(pattern, *args, **kw)

    for data in prev:
        if bool(inv) ^ bool(pattern_obj.match(data)):
            yield data