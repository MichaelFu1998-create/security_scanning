def dict_remove_value(d, v):
    """
    Recursively remove keys with a certain value from a dict
    :param d: the dictionary
    :param v: value which should be removed
    :return: formatted dictionary
    """
    dd = dict()
    for key, value in d.items():
        if not value == v:
            if isinstance(value, dict):
                dd[key] = dict_remove_value(value, v)
            elif isinstance(value, list):
                dd[key] = [dict_remove_value(i, v) for i in value]
            else:
                dd[key] = value
    return dd