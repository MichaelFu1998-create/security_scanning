def dict_search(d, k, v):
    """
    Search dictionary list by key and value
    :param d: dictionary list
    :param k: key
    :param v: value
    :return: the index of the first dictionary in the array with the specific key / value
    """
    for i in range(len(d)):
        if d[i][k] == v:
            return i
    return None