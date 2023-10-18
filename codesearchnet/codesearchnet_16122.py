def write_problems(problems, file, summarize=False, limit=0):
    """
    Write problems as restructured text to a file (or stdout/stderr).

    """
    w = file.write # convenience variable
    w("""
=================
Validation Report
=================
""")
    counts = dict() # store problem counts per problem code
    total = 0
    for i, p in enumerate(problems):
        if limit and i >= limit:
            break # bail out
        if total == 0 and not summarize:
            w("""
Problems
========
""")
        total += 1
        code = p['code']
        if code in counts:
            counts[code] += 1
        else:
            counts[code] = 1
        if not summarize:
            ptitle = '\n%s - %s\n' % (p['code'], p['message'])
            w(ptitle)
            underline = ''
            for i in range(len(ptitle.strip())):
                underline += '-'
            underline += '\n'
            w(underline)
            for k in sorted(p.viewkeys() - set(['code', 'message', 'context'])):
                w(':%s: %s\n' % (k, p[k]))
            if 'context' in p:
                c = p['context']
                for k in sorted(c.viewkeys()):
                    w(':%s: %s\n' % (k, c[k]))

    w("""
Summary
=======

Found %s%s problem%s in total.

""" % ('at least ' if limit else '', total, 's' if total != 1 else ''))
    for code in sorted(counts.viewkeys()):
        w(':%s: %s\n' % (code, counts[code]))
    return total