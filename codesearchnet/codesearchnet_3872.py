def _dict_itemstrs(dict_, **kwargs):
    """
    Create a string representation for each item in a dict.

    Example:
        >>> from ubelt.util_format import *
        >>> dict_ =  {'b': .1, 'l': 'st', 'g': 1.0, 's': 10, 'm': 0.9, 'w': .5}
        >>> kwargs = {'strkeys': True}
        >>> itemstrs, _ = _dict_itemstrs(dict_, **kwargs)
        >>> char_order = [p[0] for p in itemstrs]
        >>> assert char_order == ['b', 'g', 'l', 'm', 's', 'w']
    """
    import ubelt as ub
    explicit = kwargs.get('explicit', False)
    kwargs['explicit'] = _rectify_countdown_or_bool(explicit)
    precision = kwargs.get('precision', None)
    kvsep = kwargs.get('kvsep', ': ')
    if explicit:
        kvsep = '='

    def make_item_str(key, val):
        if explicit or kwargs.get('strkeys', False):
            key_str = six.text_type(key)
        else:
            key_str = repr2(key, precision=precision, newlines=0)

        prefix = key_str + kvsep
        kwargs['_return_info'] = True
        val_str, _leaf_info = repr2(val, **kwargs)

        # If the first line does not end with an open nest char
        # (e.g. for ndarrays), otherwise we need to worry about
        # residual indentation.
        pos = val_str.find('\n')
        first_line = val_str if pos == -1 else val_str[:pos]

        compact_brace = kwargs.get('cbr', kwargs.get('compact_brace', False))

        if compact_brace or not first_line.rstrip().endswith(tuple('([{<')):
            rest = '' if pos == -1 else val_str[pos:]
            val_str = first_line.lstrip() + rest
            if '\n' in prefix:
                # Fix issue with keys that span new lines
                item_str = prefix + val_str
            else:
                item_str = ub.hzcat([prefix, val_str])
        else:
            item_str = prefix + val_str
        return item_str, _leaf_info

    items = list(six.iteritems(dict_))
    _tups = [make_item_str(key, val) for (key, val) in items]
    itemstrs = [t[0] for t in _tups]
    max_height = max([t[1]['max_height'] for t in _tups]) if _tups else 0
    _leaf_info = {
        'max_height': max_height + 1,
    }

    sort = kwargs.get('sort', None)
    if sort is None:
        # Force ordering on unordered dicts
        sort = True
    if isinstance(dict_, collections.OrderedDict):
        # never sort ordered dicts; they are perfect just the way they are!
        sort = False
    if sort:
        itemstrs = _sort_itemstrs(items, itemstrs)
    return itemstrs, _leaf_info