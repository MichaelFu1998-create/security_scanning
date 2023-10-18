def match(prev, pattern, *args, **kw):
    """The pipe greps the data passed from previous generator according to
    given regular expression. The data passed to next pipe is MatchObject
    , dict or tuple which determined by 'to' in keyword argument.

    By default, match pipe yields MatchObject. Use 'to' in keyword argument
    to change the type of match result.

    If 'to' is dict, yield MatchObject.groupdict().
    If 'to' is tuple, yield MatchObject.groups().
    If 'to' is list, yield list(MatchObject.groups()).

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param pattern: The pattern which used to filter data.
    :type pattern: str|unicode
    :param to: What data type the result should be stored. dict|tuple|list
    :type to: type
    :returns: generator
    """
    to = 'to' in kw and kw.pop('to')
    pattern_obj = re.compile(pattern, *args, **kw)

    if to is dict:
        for data in prev:
            match = pattern_obj.match(data)
            if match is not None:
                yield match.groupdict()
    elif to is tuple:
        for data in prev:
            match = pattern_obj.match(data)
            if match is not None:
                yield match.groups()
    elif to is list:
        for data in prev:
            match = pattern_obj.match(data)
            if match is not None:
                yield list(match.groups())
    else:
        for data in prev:
            match = pattern_obj.match(data)
            if match is not None:
                yield match