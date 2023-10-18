def value_to_single_key_strokes(value):
    """Convert value to a list of key strokes
    >>> value_to_single_key_strokes(123)
    ['1', '2', '3']
    >>> value_to_single_key_strokes('123')
    ['1', '2', '3']
    >>> value_to_single_key_strokes([1, 2, 3])
    ['1', '2', '3']
    >>> value_to_single_key_strokes(['1', '2', '3'])
    ['1', '2', '3']
    Args:
        value(int|str|list)
    Returns:
        A list of string.
    """
    result = []
    if isinstance(value, Integral):
        value = str(value)

    for v in value:
        if isinstance(v, Keys):
            result.append(v.value)
        elif isinstance(v, Integral):
            result.append(str(v))
        else:
            result.append(v)
    return result