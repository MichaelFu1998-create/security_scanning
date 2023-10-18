def update_merge(d, u):
    """
    Recursively merges two dictionaries.

    Uses fabric's AttributeDict so you can reference values via dot-notation.
    e.g. env.value1.value2.value3...

    http://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    """
    import collections
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update_merge(d.get(k, dict()), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d