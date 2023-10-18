def split_at_single(text, sep, not_before=[], not_after=[]):
    """Works like text.split(sep) but separated fragments
    cant end with not_before or start with not_after"""
    n = 0
    lt, s = len(text), len(sep)
    last = 0
    while n < lt:
        if not s + n > lt:
            if sep == text[n:n + s]:
                if any(text[last:n].endswith(e) for e in not_before):
                    pass
                elif any(text[n + s:].startswith(e) for e in not_after):
                    pass
                else:
                    yield text[last:n]
                    last = n + s
                    n += s - 1
        n += 1
    yield text[last:]