def dict_as_tuple_list(d, as_list=False):
    """
    Format a dict to a list of tuples
    :param d: the dictionary
    :param as_list: return a list of lists rather than a list of tuples
    :return: formatted dictionary list
    """
    dd = list()
    for k, v in d.items():
        dd.append([k, v] if as_list else (k, v))
    return dd