def _format_dict(dict_, **kwargs):
    """
    Makes a pretty printable / human-readable string representation of a
    dictionary. In most cases this string could be evaled.

    Args:
        dict_ (dict):  a dictionary
        **kwargs: si, stritems, strkeys, strvals, sk, sv, nl, newlines, nobr,
                  nobraces, cbr, compact_brace, trailing_sep,
                  explicit, itemsep, precision, kvsep, sort

    Returns:
        Tuple[str, Dict] : retstr, _leaf_info

    Kwargs:
        sort (None): if True, sorts ALL collections and subcollections,
            note, collections with undefined orders (e.g. dicts, sets) are
            sorted by default. (default = None)
        nl (int): preferred alias for newline. can be a countdown variable
            (default = None)
        explicit (int): can be a countdown variable. if True, uses
            dict(a=b) syntax instead of {'a': b}
        nobr (bool): removes outer braces (default = False)
    """
    kwargs['_root_info'] = _rectify_root_info(kwargs.get('_root_info', None))
    kwargs['_root_info']['depth'] += 1

    stritems = kwargs.pop('si', kwargs.pop('stritems', False))
    if stritems:
        kwargs['strkeys'] = True
        kwargs['strvals'] = True

    kwargs['strkeys'] = kwargs.pop('sk', kwargs.pop('strkeys', False))
    kwargs['strvals'] = kwargs.pop('sv', kwargs.pop('strvals', False))

    newlines = kwargs.pop('nl', kwargs.pop('newlines', True))
    kwargs['nl'] = _rectify_countdown_or_bool(newlines)

    nobraces = kwargs.pop('nobr', kwargs.pop('nobraces', False))

    compact_brace = kwargs.get('cbr', kwargs.get('compact_brace', False))
    # kwargs['cbr'] = _rectify_countdown_or_bool(compact_brace)

    # Doesn't actually put in trailing comma if on same line
    trailing_sep = kwargs.get('trailsep', kwargs.get('trailing_sep', newlines > 0))
    explicit = kwargs.get('explicit', False)
    itemsep = kwargs.get('itemsep', ' ')

    if len(dict_) == 0:
        retstr = 'dict()' if explicit else '{}'
        _leaf_info = None
    else:
        itemstrs, _leaf_info = _dict_itemstrs(dict_, **kwargs)
        if nobraces:
            lbr, rbr = '', ''
        elif explicit:
            lbr, rbr = 'dict(', ')'
        else:
            lbr, rbr = '{', '}'
        retstr = _join_itemstrs(itemstrs, itemsep, newlines, _leaf_info, nobraces,
                                trailing_sep, compact_brace, lbr, rbr)
    return retstr, _leaf_info