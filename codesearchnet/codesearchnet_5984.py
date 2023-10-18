def sub_list(l):
    """
    Recursively walk a data-structure sorting any lists along the way.
    Any unknown types get mapped to string representation

    :param l: list
    :return: sorted list, where any child lists are also sorted.
    """
    r = []

    for i in l:
        if type(i) in prims:
            r.append(i)
        elif type(i) is list:
            r.append(sub_list(i))
        elif type(i) is dict:
            r.append(sub_dict(i))
        else:
            r.append(str(i))
    r = sorted(r)
    return r