def do_statement(source, start):
    """returns none if not found other functions that begin with 'do_' raise
    also this do_ type function passes white space"""
    start = pass_white(source, start)
    # start is the fist position after initial start that is not a white space or \n
    if not start < len(source):  #if finished parsing return None
        return None, start
    if any(startswith_keyword(source[start:], e) for e in {'case', 'default'}):
        return None, start
    rest = source[start:]
    for key, meth in KEYWORD_METHODS.iteritems(
    ):  # check for statements that are uniquely defined by their keywords
        if rest.startswith(key):
            # has to startwith this keyword and the next letter after keyword must be either EOF or not in IDENTIFIER_PART
            if len(key) == len(rest) or rest[len(key)] not in IDENTIFIER_PART:
                return meth(source, start)
    if rest[0] == '{':  #Block
        return do_block(source, start)
    # Now only label and expression left
    cand = parse_identifier(source, start, False)
    if cand is not None:  # it can mean that its a label
        label, cand_start = cand
        cand_start = pass_white(source, cand_start)
        if source[cand_start] == ':':
            return do_label(source, start)
    return do_expression(source, start)