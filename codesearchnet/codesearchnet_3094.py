def parse_identifier(source, start, throw=True):
    """passes white space from start and returns first identifier,
       if identifier invalid and throw raises SyntaxError otherwise returns None"""
    start = pass_white(source, start)
    end = start
    if not end < len(source):
        if throw:
            raise SyntaxError('Missing identifier!')
        return None
    if source[end] not in IDENTIFIER_START:
        if throw:
            raise SyntaxError('Invalid identifier start: "%s"' % source[end])
        return None
    end += 1
    while end < len(source) and source[end] in IDENTIFIER_PART:
        end += 1
    if not is_valid_lval(source[start:end]):
        if throw:
            raise SyntaxError(
                'Invalid identifier name: "%s"' % source[start:end])
        return None
    return source[start:end], end