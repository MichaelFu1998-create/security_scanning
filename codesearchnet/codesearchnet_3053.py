def bracket_split(source, brackets=('()', '{}', '[]'), strip=False):
    """DOES NOT RETURN EMPTY STRINGS (can only return empty bracket content if strip=True)"""
    starts = [e[0] for e in brackets]
    in_bracket = 0
    n = 0
    last = 0
    while n < len(source):
        e = source[n]
        if not in_bracket and e in starts:
            in_bracket = 1
            start = n
            b_start, b_end = brackets[starts.index(e)]
        elif in_bracket:
            if e == b_start:
                in_bracket += 1
            elif e == b_end:
                in_bracket -= 1
                if not in_bracket:
                    if source[last:start]:
                        yield source[last:start]
                    last = n + 1
                    yield source[start + strip:n + 1 - strip]
        n += 1
    if source[last:]:
        yield source[last:]