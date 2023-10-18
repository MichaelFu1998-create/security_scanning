def multitype_sort(a):
    """
    Sort elements of multiple types

    x is assumed to contain elements of different types, such that
    plain sort would raise a `TypeError`.

    Parameters
    ----------
    a : array-like
        Array of items to be sorted

    Returns
    -------
    out : list
        Items sorted within their type groups.
    """
    types = defaultdict(list)
    numbers = {int, float, complex}

    for x in a:
        t = type(x)
        if t in numbers:
            types['number'].append(x)
        else:
            types[t].append(x)

    for t in types:
        types[t] = np.sort(types[t])

    return list(chain(*(types[t] for t in types)))