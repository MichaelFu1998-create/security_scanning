def parse_exponent(source, start):
    """returns end of exponential, raises SyntaxError if failed"""
    if not source[start] in {'e', 'E'}:
        if source[start] in IDENTIFIER_PART:
            raise SyntaxError('Invalid number literal!')
        return start
    start += 1
    if source[start] in {'-', '+'}:
        start += 1
    FOUND = False
    # we need at least one dig after exponent
    while source[start] in NUMS:
        FOUND = True
        start += 1
    if not FOUND or source[start] in IDENTIFIER_PART:
        raise SyntaxError('Invalid number literal!')
    return start