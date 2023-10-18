def _randone(d, limit=20, grouprefs=None):
    if grouprefs is None:
        grouprefs = {}
    """docstring for _randone"""
    ret = ''
    for i in d:
        if i[0] == sre_parse.IN:
            ret += choice(_in(i[1]))
        elif i[0] == sre_parse.LITERAL:
            ret += unichr(i[1])
        elif i[0] == sre_parse.CATEGORY:
            ret += choice(CATEGORIES.get(i[1], ['']))
        elif i[0] == sre_parse.ANY:
            ret += choice(CATEGORIES['category_any'])
        elif i[0] == sre_parse.MAX_REPEAT or i[0] == sre_parse.MIN_REPEAT:
            if i[1][1] + 1 - i[1][0] >= limit:
                min, max = i[1][0], i[1][0] + limit - 1
            else:
                min, max = i[1][0], i[1][1]
            for _ in range(randint(min, max)):
                ret += _randone(list(i[1][2]), limit, grouprefs)
        elif i[0] == sre_parse.BRANCH:
            ret += _randone(choice(i[1][1]), limit, grouprefs)
        elif i[0] == sre_parse.SUBPATTERN or i[0] == sre_parse.ASSERT:
            subexpr = i[1][1]
            if IS_PY36_OR_GREATER and i[0] == sre_parse.SUBPATTERN:
                subexpr = i[1][3]
            subp = _randone(subexpr, limit, grouprefs)
            if i[1][0]:
                grouprefs[i[1][0]] = subp
            ret += subp
        elif i[0] == sre_parse.AT:
            continue
        elif i[0] == sre_parse.NOT_LITERAL:
            c = list(CATEGORIES['category_any'])
            if unichr(i[1]) in c:
                c.remove(unichr(i[1]))
            ret += choice(c)
        elif i[0] == sre_parse.GROUPREF:
            ret += grouprefs[i[1]]
        elif i[0] == sre_parse.ASSERT_NOT:
            pass
        else:
            print('[!] cannot handle expression "%s"' % str(i))

    return ret