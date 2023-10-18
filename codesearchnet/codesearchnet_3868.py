def repr2(data, **kwargs):
    """
    Makes a pretty and easy-to-doctest string representation!

    This is an alternative to repr, and `pprint.pformat` that attempts to be
    both more configurable and generate output that is consistent between
    python versions.

    Notes:
        This function has many keyword arguments that can be used to customize
        the final representation. For convinience some of the more frequently
        used kwargs have short aliases. See `Args` for more details.

    Args:
        data (object): an arbitrary python object
        **kwargs: see `the Kwargs` section

    Kwargs:
        si, stritems, (bool):
            dict/list items use str instead of repr

        strkeys, sk (bool):
            dict keys use str instead of repr

        strvals, sv (bool):
            dict values use str instead of repr

        nl, newlines (int | bool):
            number of top level nestings to place a newline after. If true all
            items are followed by newlines regardless of nesting level.
            Defaults to 1 for lists and True for dicts.

        nobr, nobraces (bool, default=False):
            if True, text will not contain outer braces for containers

        cbr, compact_brace (bool, default=False):
            if True, braces are compactified (i.e. they will not have newlines
            placed directly after them, think java / K&R / 1TBS)

        trailsep, trailing_sep (bool):
            if True, a separator is placed after the last item in a sequence.
            By default this is True if there are any `nl > 0`.

        explicit (bool, default=False):
            changes dict representation from `{k1: v1, ...}` to
            `dict(k1=v1, ...)`.

        precision (int, default=None):
            if specified floats are formatted with this precision

        kvsep (str, default=': '):
            separator between keys and values

        itemsep (str, default=' '):
            separator between items

        sort (bool):
            if True, attempts to sort all unordered collections in the returned
            text. NOTE: currently if True this will sort lists, this may not be
            a correct thing to do, as such the behavior of this arg is subject
            to change.

        suppress_small (bool):
            passed to `numpy.array2string` for ndarrays

        max_line_width (int):
            passed to `numpy.array2string` for ndarrays

        with_dtype (bool):
            only relevant to ndarrays. if True includes the dtype.

    Returns:
        str: outstr: output string

    Notes:
        There are also internal kwargs, which should not be used:
            _return_info (bool):  return information about child context
            _root_info (depth): information about parent context

    CommandLine:
        python -m ubelt.util_format repr2:0
        python -m ubelt.util_format repr2:1

    Example:
        >>> from ubelt.util_format import *
        >>> import ubelt as ub
        >>> dict_ = {
        ...     'custom_types': [slice(0, 1, None), 1/3],
        ...     'nest_dict': {'k1': [1, 2, {3: {4, 5}}],
        ...                   'key2': [1, 2, {3: {4, 5}}],
        ...                   'key3': [1, 2, {3: {4, 5}}],
        ...                   },
        ...     'nest_dict2': {'k': [1, 2, {3: {4, 5}}]},
        ...     'nested_tuples': [tuple([1]), tuple([2, 3]), frozenset([4, 5, 6])],
        ...     'one_tup': tuple([1]),
        ...     'simple_dict': {'spam': 'eggs', 'ham': 'jam'},
        ...     'simple_list': [1, 2, 'red', 'blue'],
        ...     'odict': ub.odict([(1, '1'), (2, '2')]),
        ... }
        >>> result = repr2(dict_, nl=3, precision=2); print(result)
        >>> result = repr2(dict_, nl=2, precision=2); print(result)
        >>> result = repr2(dict_, nl=1, precision=2); print(result)
        >>> result = repr2(dict_, nl=1, precision=2, itemsep='', explicit=True); print(result)
        >>> result = repr2(dict_, nl=1, precision=2, nobr=1, itemsep='', explicit=True); print(result)
        >>> result = repr2(dict_, nl=3, precision=2, cbr=True); print(result)
        >>> result = repr2(dict_, nl=3, precision=2, si=True); print(result)
        >>> result = repr2(dict_, nl=3, sort=True); print(result)
        >>> result = repr2(dict_, nl=3, sort=False, trailing_sep=False); print(result)
        >>> result = repr2(dict_, nl=3, sort=False, trailing_sep=False, nobr=True); print(result)

    Example:
        >>> from ubelt.util_format import *
        >>> def _nest(d, w):
        ...     if d == 0:
        ...         return {}
        ...     else:
        ...         return {'n{}'.format(d): _nest(d - 1, w + 1), 'm{}'.format(d): _nest(d - 1, w + 1)}
        >>> dict_ = _nest(d=4, w=1)
        >>> result = repr2(dict_, nl=6, precision=2, cbr=1)
        >>> print('---')
        >>> print(result)
        >>> result = repr2(dict_, nl=-1, precision=2)
        >>> print('---')
        >>> print(result)
    """
    custom_extensions = kwargs.get('extensions', None)

    _return_info = kwargs.get('_return_info', False)
    kwargs['_root_info'] = _rectify_root_info(kwargs.get('_root_info', None))

    outstr = None
    _leaf_info = None

    if custom_extensions:
        func = custom_extensions.lookup(data)
        if func is not None:
            outstr = func(data, **kwargs)

    if outstr is None:
        if isinstance(data, dict):
            outstr, _leaf_info = _format_dict(data, **kwargs)
        elif isinstance(data, (list, tuple, set, frozenset)):
            outstr, _leaf_info = _format_list(data, **kwargs)

    if outstr is None:
        # check any globally registered functions for special formatters
        func = _FORMATTER_EXTENSIONS.lookup(data)
        if func is not None:
            outstr = func(data, **kwargs)
        else:
            outstr = _format_object(data, **kwargs)

    if _return_info:
        _leaf_info = _rectify_leaf_info(_leaf_info)
        return outstr, _leaf_info
    else:
        return outstr