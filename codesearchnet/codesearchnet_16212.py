def value_to_key_strokes(value):
    """Convert value to a list of key strokes
    >>> value_to_key_strokes(123)
    ['123']
    >>> value_to_key_strokes('123')
    ['123']
    >>> value_to_key_strokes([1, 2, 3])
    ['123']
    >>> value_to_key_strokes(['1', '2', '3'])
    ['123']

    Args:
        value(int|str|list)

    Returns:
        A list of string.
    """
    result = ''
    if isinstance(value, Integral):
        value = str(value)

    for v in value:
        if isinstance(v, Keys):
            result += v.value
        elif isinstance(v, Integral):
            result += str(v)
        else:
            result += v
    return [result]