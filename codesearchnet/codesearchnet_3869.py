def _format_list(list_, **kwargs):
    """
    Makes a pretty printable / human-readable string representation of a
    sequence. In most cases this string could be evaled.

    Args:
        list_ (list): input list
        **kwargs: nl, newlines, packed, nobr, nobraces, itemsep, trailing_sep,
            strvals indent_, precision, use_numpy, with_dtype, force_dtype,
            stritems, strkeys, explicit, sort, key_order, maxlen

    Returns:
        Tuple[str, Dict] : retstr, _leaf_info

    Example:
        >>> print(_format_list([])[0])
        []
        >>> print(_format_list([], nobr=True)[0])
        []
        >>> print(_format_list([1], nl=0)[0])
        [1]
        >>> print(_format_list([1], nobr=True)[0])
        1,
    """
    kwargs['_root_info'] = _rectify_root_info(kwargs.get('_root_info', None))
    kwargs['_root_info']['depth'] += 1

    newlines = kwargs.pop('nl', kwargs.pop('newlines', 1))
    kwargs['nl'] = _rectify_countdown_or_bool(newlines)

    nobraces = kwargs.pop('nobr', kwargs.pop('nobraces', False))

    itemsep = kwargs.get('itemsep', ' ')

    compact_brace = kwargs.get('cbr', kwargs.get('compact_brace', False))
    # kwargs['cbr'] = _rectify_countdown_or_bool(compact_brace)

    itemstrs, _leaf_info = _list_itemstrs(list_, **kwargs)
    if len(itemstrs) == 0:
        nobraces = False  # force braces to prevent empty output

    is_tuple = isinstance(list_, tuple)
    is_set = isinstance(list_, (set, frozenset,))
    if nobraces:
        lbr, rbr = '', ''
    elif is_tuple:
        lbr, rbr  = '(', ')'
    elif is_set:
        lbr, rbr  = '{', '}'
    else:
        lbr, rbr  = '[', ']'

    # Doesn't actually put in trailing comma if on same line
    trailing_sep = kwargs.get('trailsep', kwargs.get('trailing_sep', newlines > 0 and len(itemstrs)))

    # The trailing separator is always needed for single item tuples
    if is_tuple and len(list_) <= 1:
        trailing_sep = True

    if len(itemstrs) == 0:
        newlines = False

    retstr = _join_itemstrs(itemstrs, itemsep, newlines, _leaf_info, nobraces,
                            trailing_sep, compact_brace, lbr, rbr)
    return retstr, _leaf_info