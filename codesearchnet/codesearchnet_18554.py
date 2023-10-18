def sub(prev, pattern, repl, *args, **kw):
    """sub pipe is a wrapper of re.sub method.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param pattern: The pattern string.
    :type pattern: str|unicode
    :param repl: Check repl argument in re.sub method.
    :type repl: str|unicode|callable
    """
    count = 0 if 'count' not in kw else kw.pop('count')
    pattern_obj = re.compile(pattern, *args, **kw)
    for s in prev:
        yield pattern_obj.sub(repl, s, count=count)