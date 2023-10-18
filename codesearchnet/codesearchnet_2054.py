def filter(names, pat):
    """Return the subset of the list NAMES that match PAT"""
    import os
    # import posixpath
    result=[]
    # pat=os.path.normcase(pat)
    try:
        re_pat = _cache[pat]
    except KeyError:
        res = translate(pat)
        if len(_cache) >= _MAXCACHE:
            # _cache.clear()
            globals()['_cache'] = {}
        _cache[pat] = re_pat = re.compile(res)
    match = re_pat.match
    # if os.path is posixpath:
    if 1:
        # normcase on posix is NOP. Optimize it away from the loop.
        for name in names:
            if match(name):
                result.append(name)
    else:
        for name in names:
            if match(os.path.normcase(name)):
                result.append(name)
    return result