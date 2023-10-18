def replacement_template(rep, source, span, npar):
    """Takes the replacement template and some info about the match and returns filled template
       """
    n = 0
    res = ''
    while n < len(rep) - 1:
        char = rep[n]
        if char == '$':
            if rep[n + 1] == '$':
                res += '$'
                n += 2
                continue
            elif rep[n + 1] == '`':
                # replace with string that is BEFORE match
                res += source[:span[0]]
                n += 2
                continue
            elif rep[n + 1] == '\'':
                # replace with string that is AFTER match
                res += source[span[1]:]
                n += 2
                continue
            elif rep[n + 1] in DIGS:
                dig = rep[n + 1]
                if n + 2 < len(rep) and rep[n + 2] in DIGS:
                    dig += rep[n + 2]
                num = int(dig)
                # we will not do any replacements if we dont have this npar or dig is 0
                if not num or num > len(npar):
                    res += '$' + dig
                else:
                    # None - undefined has to be replaced with ''
                    res += npar[num - 1] if npar[num - 1] else ''
                n += 1 + len(dig)
                continue
        res += char
        n += 1
    if n < len(rep):
        res += rep[-1]
    return res