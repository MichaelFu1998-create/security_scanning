def except_token(source, start, token, throw=True):
    """Token can be only a single char. Returns position after token if found. Otherwise raises syntax error if throw
    otherwise returns None"""
    start = pass_white(source, start)
    if start < len(source) and source[start] == token:
        return start + 1
    if throw:
        raise SyntaxError('Missing token. Expected %s' % token)
    return None