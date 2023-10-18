def except_keyword(source, start, keyword):
    """ Returns position after keyword if found else None
        Note: skips white space"""
    start = pass_white(source, start)
    kl = len(keyword)  #keyword len
    if kl + start > len(source):
        return None
    if source[start:start + kl] != keyword:
        return None
    if kl + start < len(source) and source[start + kl] in IDENTIFIER_PART:
        return None
    return start + kl