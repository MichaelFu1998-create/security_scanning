def sub_dict(d):
    """
    Recursively walk a data-structure sorting any lists along the way.
    Any unknown types get mapped to string representation

    :param d: dict
    :return: dict where any lists, even those buried deep in the structure, have been sorted.
    """
    r = {}
    for k in d:
        if type(d[k]) in prims:
            r[k] = d[k]
        elif type(d[k]) is list:
            r[k] = sub_list(d[k])
        elif type(d[k]) is dict:
            r[k] = sub_dict(d[k])
        else:
            r[k] = str(d[k])
    return r