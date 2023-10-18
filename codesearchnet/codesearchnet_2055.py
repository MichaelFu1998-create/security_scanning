def fnmatchcase(name, pat):
    """Test whether FILENAME matches PATTERN, including case.

    This is a version of fnmatch() which doesn't case-normalize
    its arguments.
    """

    try:
        re_pat = _cache[pat]
    except KeyError:
        res = translate(pat)
        if len(_cache) >= _MAXCACHE:
            # _cache.clear()
            globals()['_cache'] = {}
        _cache[pat] = re_pat = re.compile(res)
    return re_pat.match(name) is not None