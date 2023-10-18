def dict_sort(d, k):
    """
    Sort a dictionary list by key
    :param d: dictionary list
    :param k: key
    :return: sorted dictionary list
    """
    return sorted(d.copy(), key=lambda i: i[k])