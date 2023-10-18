def pass_bracket(source, start, bracket='()'):
    """Returns content of brackets with brackets and first pos after brackets
     if source[start] is followed by some optional white space and brackets.
     Otherwise None"""
    e = bracket_split(source[start:], [bracket], False)
    try:
        cand = e.next()
    except StopIteration:
        return None, None
    if not cand.strip():  #white space...
        try:
            res = e.next()
            return res, start + len(cand) + len(res)
        except StopIteration:
            return None, None
    elif cand[-1] == bracket[1]:
        return cand, start + len(cand)
    else:
        return None, None