def resplit(prev, pattern, *args, **kw):
    """The resplit pipe split previous pipe input by regular expression.

    Use 'maxsplit' keyword argument to limit the number of split.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param pattern: The pattern which used to split string.
    :type pattern: str|unicode
    """
    maxsplit = 0 if 'maxsplit' not in kw else kw.pop('maxsplit')
    pattern_obj = re.compile(pattern, *args, **kw)
    for s in prev:
        yield pattern_obj.split(s, maxsplit=maxsplit)