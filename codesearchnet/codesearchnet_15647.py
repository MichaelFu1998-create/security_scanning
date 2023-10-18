def dict_remove_key(d, k):
    """
    Recursively remove a key from a dict
    :param d: the dictionary
    :param k: key which should be removed
    :return: formatted dictionary
    """
    dd = dict()
    for key, value in d.items():
        if not key == k:
            if isinstance(value, dict):
                dd[key] = dict_remove_key(value, k)
            elif isinstance(value, list):
                dd[key] = [dict_remove_key(i, k) for i in value]
            else:
                dd[key] = value
    return dd