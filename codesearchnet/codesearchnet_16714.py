def fix_lamdaline(source):
    """Remove the last redundant token from lambda expression

    lambda x: return x)
                      ^
    Return string without irrelevant tokens
    returned from inspect.getsource on lamda expr returns
    """

    # Using undocumented generate_tokens due to a tokenize.tokenize bug
    # See https://bugs.python.org/issue23297
    strio = io.StringIO(source)
    gen = tokenize.generate_tokens(strio.readline)

    tkns = []
    try:
        for t in gen:
            tkns.append(t)
    except tokenize.TokenError:
        pass

    # Find the position of 'lambda'
    lambda_pos = [(t.type, t.string) for t in tkns].index(
        (tokenize.NAME, "lambda")
    )

    # Ignore tokes before 'lambda'
    tkns = tkns[lambda_pos:]

    # Find the position of th las OP
    lastop_pos = (
        len(tkns) - 1 - [t.type for t in tkns[::-1]].index(tokenize.OP)
    )
    lastop = tkns[lastop_pos]

    # Remove OP from the line
    fiedlineno = lastop.start[0]
    fixedline = lastop.line[: lastop.start[1]] + lastop.line[lastop.end[1] :]

    tkns = tkns[:lastop_pos]

    fixedlines = ""
    last_lineno = 0
    for t in tkns:
        if last_lineno == t.start[0]:
            continue
        elif t.start[0] == fiedlineno:
            fixedlines += fixedline
            last_lineno = t.start[0]
        else:
            fixedlines += t.line
            last_lineno = t.start[0]

    return fixedlines