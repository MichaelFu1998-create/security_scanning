def append_dict_values(list_of_dicts, keys=None):
    """
    Return a dict of lists from a list of dicts with the same keys.
    For each dict in list_of_dicts with look for the values of the
    given keys and append it to the output dict.

    Parameters
    ----------
    list_of_dicts: list of dicts

    keys: list of str
        List of keys to create in the output dict
        If None will use all keys in the first element of list_of_dicts
    Returns
    -------
    DefaultOrderedDict of lists
    """
    if keys is None:
        keys = list(list_of_dicts[0].keys())

    dict_of_lists = DefaultOrderedDict(list)
    for d in list_of_dicts:
        for k in keys:
            dict_of_lists[k].append(d[k])
    return dict_of_lists