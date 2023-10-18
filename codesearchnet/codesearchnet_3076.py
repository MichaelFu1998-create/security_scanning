def is_lval(t):
    """Does not chceck whether t is not resticted or internal"""
    if not t:
        return False
    i = iter(t)
    if i.next() not in IDENTIFIER_START:
        return False
    return all(e in IDENTIFIER_PART for e in i)