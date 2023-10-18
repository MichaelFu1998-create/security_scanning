def is_object(n, last):
    """n may be the inside of block or object.
       last is the code before object"""
    if is_empty_object(n, last):
        return True
    if not n.strip():
        return False
    #Object contains lines of code so it cant be an object
    if len(argsplit(n, ';')) > 1:
        return False
    cands = argsplit(n, ',')
    if not cands[-1].strip():
        return True  # {xxxx,} empty after last , it must be an object
    for cand in cands:
        cand = cand.strip()
        # separate each candidate element at : in dict and check whether they are correct...
        kv = argsplit(cand, ':')
        if len(
                kv
        ) > 2:  # set the len of kv to 2 because of this stupid : expression
            kv = kv[0], ':'.join(kv[1:])

        if len(kv) == 2:
            # key value pair, check whether not label or ?:
            k, v = kv
            if not is_lval(k.strip()):
                return False
            v = v.strip()
            if v.startswith('function'):
                continue
            #will fail on label... {xxx: while {}}
            if v[0] == '{':  # value cant be a code block
                return False
            for e in KEYWORD_METHODS:
                # if v starts with any statement then return false
                if v.startswith(e) and len(e) < len(v) and v[len(
                        e)] not in IDENTIFIER_PART:
                    return False
        elif not (cand.startswith('set ') or cand.startswith('get ')):
            return False
    return True