def _compare_lists(list1, list2, custom_cmp):
    """Compare twolists using given comparing function.

    :param list1: first list to compare
    :param list2: second list to compare
    :param custom_cmp: a function taking two arguments (element of
        list 1, element of list 2) and
    :return: True or False depending if the values are the same
    """
    if len(list1) != len(list2):
        return False
    for element1, element2 in zip(list1, list2):
        if not custom_cmp(element1, element2):
            return False
    return True