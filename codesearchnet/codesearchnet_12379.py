def merge_dicts(d1, d2, _path=None):
    """
    Merge dictionary d2 into d1, overriding entries in d1 with values from d2.

    d1 is mutated.

    _path is for internal, recursive use.
    """
    if _path is None:
        _path = ()
    if isinstance(d1, dict) and isinstance(d2, dict):
        for k, v in d2.items():
            if isinstance(v, MissingValue) and v.name is None:
                v.name = '.'.join(_path + (k,))

            if isinstance(v, DeletedValue):
                d1.pop(k, None)
            elif k not in d1:
                if isinstance(v, dict):
                    d1[k] = merge_dicts({}, v, _path + (k,))
                else:
                    d1[k] = v
            else:
                if isinstance(d1[k], dict) and isinstance(v, dict):
                    d1[k] = merge_dicts(d1[k], v, _path + (k,))
                elif isinstance(d1[k], list) and isinstance(v, list):
                    # Lists are only supported as leaves
                    d1[k] += v
                elif isinstance(d1[k], MissingValue):
                    d1[k] = v
                elif d1[k] is None:
                    d1[k] = v
                elif type(d1[k]) == type(v):
                    d1[k] = v
                else:
                    raise TypeError('Refusing to replace a %s with a %s'
                                    % (type(d1[k]), type(v)))
    else:
        raise TypeError('Cannot merge a %s with a %s' % (type(d1), type(d2)))

    return d1