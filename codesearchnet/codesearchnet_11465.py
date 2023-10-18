def merge_dict(dict1, dict2, merge_lists=False):
    """
    Recursively merges the contents of two dictionaries into a new dictionary.

    When both input dictionaries share a key, the value from ``dict2`` is
    kept.

    :param dict1: the first dictionary
    :type dict1: dict
    :param dict2: the second dictionary
    :type dict2: dict
    :param merge_lists:
        when this function encounters a key that contains lists in both input
        dictionaries, this parameter dictates whether or not those lists should
        be merged. If not specified, defaults to ``False``.
    :type merge_lists: bool
    :returns: dict
    """

    merged = dict(dict1)

    for key, value in iteritems(dict2):
        if isinstance(merged.get(key), dict):
            merged[key] = merge_dict(merged[key], value)
        elif merge_lists and isinstance(merged.get(key), list):
            merged[key] = merge_list(merged[key], value)
        else:
            merged[key] = value

    return merged