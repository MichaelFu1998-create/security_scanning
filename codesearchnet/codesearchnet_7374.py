def _gen(d, limit=20, count=False, grouprefs=None):
    """docstring for _gen"""
    if grouprefs is None:
        grouprefs = {}
    ret = ['']
    strings = 0
    literal = False
    for i in d:
        if i[0] == sre_parse.IN:
            subs = _in(i[1])
            if count:
                strings = (strings or 1) * len(subs)
            ret = comb(ret, subs)
        elif i[0] == sre_parse.LITERAL:
            literal = True
            ret = mappend(ret, unichr(i[1]))
        elif i[0] == sre_parse.CATEGORY:
            subs = CATEGORIES.get(i[1], [''])
            if count:
                strings = (strings or 1) * len(subs)
            ret = comb(ret, subs)
        elif i[0] == sre_parse.ANY:
            subs = CATEGORIES['category_any']
            if count:
                strings = (strings or 1) * len(subs)
            ret = comb(ret, subs)
        elif i[0] == sre_parse.MAX_REPEAT or i[0] == sre_parse.MIN_REPEAT:
            items = list(i[1][2])
            if i[1][1] + 1 - i[1][0] >= limit:
                r1 = i[1][0]
                r2 = i[1][0] + limit
            else:
                r1 = i[1][0]
                r2 = i[1][1] + 1
            ran = range(r1, r2)
            if count:
                branch_count = 0
                for p in ran:
                    branch_count += pow(_gen(items, limit, True, grouprefs), p)
                strings = (strings or 1) * branch_count

            ret = prods(ret, ran, items, limit, grouprefs)
        elif i[0] == sre_parse.BRANCH:
            if count:
                for x in i[1][1]:
                    strings += _gen(x, limit, True, grouprefs) or 1
            ret = concit(ret, i[1][1], limit, grouprefs)
        elif i[0] == sre_parse.SUBPATTERN or i[0] == sre_parse.ASSERT:
            subexpr = i[1][1]
            if IS_PY36_OR_GREATER and i[0] == sre_parse.SUBPATTERN:
                subexpr = i[1][3]
            if count:
                strings = (
                    strings or 1) * (sum(ggen([0], _gen, subexpr, limit=limit, count=True, grouprefs=grouprefs)) or 1)
            ret = ggen(ret, _gen, subexpr, limit=limit, count=False, grouprefs=grouprefs, groupref=i[1][0])
        # ignore ^ and $
        elif i[0] == sre_parse.AT:
            continue
        elif i[0] == sre_parse.NOT_LITERAL:
            subs = list(CATEGORIES['category_any'])
            if unichr(i[1]) in subs:
                subs.remove(unichr(i[1]))
            if count:
                strings = (strings or 1) * len(subs)
            ret = comb(ret, subs)
        elif i[0] == sre_parse.GROUPREF:
            ret = dappend(ret, grouprefs, i[1])
        elif i[0] == sre_parse.ASSERT_NOT:
            pass
        else:
            print('[!] cannot handle expression ' + repr(i))

    if count:
        if strings == 0 and literal:
            inc = True
            for i in d:
                if i[0] not in (sre_parse.AT, sre_parse.LITERAL):
                    inc = False
            if inc:
                strings = 1
        return strings

    return ret