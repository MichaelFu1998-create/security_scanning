def _dict_diff(d1, d2):
    """
    Produce a dict that includes all the keys in d2 that represent different values in d1, as well as values that
    aren't in d1.

    :param dict d1: First dict
    :param dict d2: Dict to compare with
    :rtype: dict
    """
    d = {}
    for key in set(d1).intersection(set(d2)):
        if d2[key] != d1[key]:
            d[key] = d2[key]
    for key in set(d2).difference(set(d1)):
        d[key] = d2[key]
    return d