def merge_list(list1, list2):
    """
    Merges the contents of two lists into a new list.

    :param list1: the first list
    :type list1: list
    :param list2: the second list
    :type list2: list
    :returns: list
    """

    merged = list(list1)

    for value in list2:
        if value not in merged:
            merged.append(value)

    return merged