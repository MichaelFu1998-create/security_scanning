def set_nested(data, value, *keys):
    """Assign to a nested dictionary.

    :param dict data: Dictionary to mutate
    :param value: Value to set
    :param list *keys: List of nested keys

    >>> data = {}
    >>> set_nested(data, 'hi', 'k0', 'k1', 'k2')
    >>> data
    {'k0': {'k1': {'k2': 'hi'}}}

    """
    if len(keys) == 1:
        data[keys[0]] = value
    else:
        if keys[0] not in data:
            data[keys[0]] = {}
        set_nested(data[keys[0]], value, *keys[1:])