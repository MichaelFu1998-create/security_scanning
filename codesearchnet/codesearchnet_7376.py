def sre_to_string(sre_obj, paren=True):
    """sre_parse object to string

    :param sre_obj: Output of sre_parse.parse()
    :type sre_obj: list
    :rtype: str
    """
    ret = u''
    for i in sre_obj:
        if i[0] == sre_parse.IN:
            prefix = ''
            if len(i[1]) and i[1][0][0] == sre_parse.NEGATE:
                prefix = '^'
            ret += u'[{0}{1}]'.format(prefix, sre_to_string(i[1], paren=paren))
        elif i[0] == sre_parse.LITERAL:
            u = unichr(i[1])
            ret += u if u not in sre_parse.SPECIAL_CHARS else '\\{0}'.format(u)
        elif i[0] == sre_parse.CATEGORY:
            ret += REVERSE_CATEGORIES[i[1]]
        elif i[0] == sre_parse.ANY:
            ret += '.'
        elif i[0] == sre_parse.BRANCH:
            # TODO simplifications here
            parts = [sre_to_string(x, paren=paren) for x in i[1][1]]
            if not any(parts):
                continue
            if i[1][0]:
                if len(parts) == 1:
                    paren = False
                prefix = ''
            else:
                prefix = '?:'
            branch = '|'.join(parts)
            if paren:
                ret += '({0}{1})'.format(prefix, branch)
            else:
                ret += '{0}'.format(branch)
        elif i[0] == sre_parse.SUBPATTERN:
            subexpr = i[1][1]
            if IS_PY36_OR_GREATER and i[0] == sre_parse.SUBPATTERN:
                subexpr = i[1][3]
            if i[1][0]:
                ret += '({0})'.format(sre_to_string(subexpr, paren=False))
            else:
                ret += '{0}'.format(sre_to_string(subexpr, paren=paren))
        elif i[0] == sre_parse.NOT_LITERAL:
            ret += '[^{0}]'.format(unichr(i[1]))
        elif i[0] == sre_parse.MAX_REPEAT:
            if i[1][0] == i[1][1]:
                range_str = '{{{0}}}'.format(i[1][0])
            else:
                if i[1][0] == 0 and i[1][1] - i[1][0] == sre_parse.MAXREPEAT:
                    range_str = '*'
                elif i[1][0] == 1 and i[1][1] - i[1][0] == sre_parse.MAXREPEAT - 1:
                    range_str = '+'
                else:
                    range_str = '{{{0},{1}}}'.format(i[1][0], i[1][1])
            ret += sre_to_string(i[1][2], paren=paren) + range_str
        elif i[0] == sre_parse.MIN_REPEAT:
            if i[1][0] == 0 and i[1][1] == sre_parse.MAXREPEAT:
                range_str = '*?'
            elif i[1][0] == 1 and i[1][1] == sre_parse.MAXREPEAT:
                range_str = '+?'
            elif i[1][1] == sre_parse.MAXREPEAT:
                range_str = '{{{0},}}?'.format(i[1][0])
            else:
                range_str = '{{{0},{1}}}?'.format(i[1][0], i[1][1])
            ret += sre_to_string(i[1][2], paren=paren) + range_str
        elif i[0] == sre_parse.GROUPREF:
            ret += '\\{0}'.format(i[1])
        elif i[0] == sre_parse.AT:
            if i[1] == sre_parse.AT_BEGINNING:
                ret += '^'
            elif i[1] == sre_parse.AT_END:
                ret += '$'
        elif i[0] == sre_parse.NEGATE:
            pass
        elif i[0] == sre_parse.RANGE:
            ret += '{0}-{1}'.format(unichr(i[1][0]), unichr(i[1][1]))
        elif i[0] == sre_parse.ASSERT:
            if i[1][0]:
                ret += '(?={0})'.format(sre_to_string(i[1][1], paren=False))
            else:
                ret += '{0}'.format(sre_to_string(i[1][1], paren=paren))
        elif i[0] == sre_parse.ASSERT_NOT:
            pass
        else:
            print('[!] cannot handle expression "%s"' % str(i))
    return ret