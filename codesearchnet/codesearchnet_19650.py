def update_nested_dict(a, b):
    """
    update nested dict `a` with another dict b.
    usage::

        >>> a = {'x' : { 'y': 1}}
        >>> b = {'x' : {'z':2, 'y':3}, 'w': 4}
        >>> update_nested_dict(a,b)
        {'x': {'y': 3, 'z': 2}, 'w': 4}

    """
    for k, v in b.iteritems():
        if isinstance(v, dict):
            d = a.setdefault(k, {})
            update_nested_dict(d, v)
        else:
            a[k] = v
    return a