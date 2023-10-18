def _pred_pattern(match='*', exclude='', patterntype='fnmatch'):

    """ internal use """
    m, x = match, exclude
    if m == '*':
        if not x:
            pred = lambda n: True
        else:
            x = [x] if _is_str(x) else x
            matcher = get_match_fun(x, patterntype)
            pred = lambda n: not matcher(n)
    else:
        m = [m] if _is_str(m) else m
        if not x:
            matcher = get_match_fun(m, patterntype)
            pred = lambda n: matcher(n)
        else:
            x = [x] if _is_str(x) else x
            matcher_m = get_match_fun(m, patterntype)
            matcher_x = get_match_fun(x, patterntype)
            pred = lambda n: matcher_m(n) and not matcher_x(n)

    return pred