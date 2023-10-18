def _rectify_base(base):
    """
    transforms base shorthand into the full list representation

    Example:
        >>> assert _rectify_base(NoParam) is DEFAULT_ALPHABET
        >>> assert _rectify_base('hex') is _ALPHABET_16
        >>> assert _rectify_base('abc') is _ALPHABET_26
        >>> assert _rectify_base(10) is _ALPHABET_10
        >>> assert _rectify_base(['1', '2']) == ['1', '2']
        >>> import pytest
        >>> assert pytest.raises(TypeError, _rectify_base, 'uselist')
    """
    if base is NoParam or base == 'default':
        return DEFAULT_ALPHABET
    elif base in [26, 'abc', 'alpha']:
        return _ALPHABET_26
    elif base in [16, 'hex']:
        return _ALPHABET_16
    elif base in [10, 'dec']:
        return _ALPHABET_10
    else:
        if not isinstance(base, (list, tuple)):
            raise TypeError(
                'Argument `base` must be a key, list, or tuple; not {}'.format(
                    type(base)))
        return base