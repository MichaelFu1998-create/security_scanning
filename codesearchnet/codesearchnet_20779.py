def is_disjoint(set1, set2, warn):
    """
    Checks if elements of set2 are in set1.

    :param set1: a set of values
    :param set2: a set of values
    :param warn: the error message that should be thrown
     when the sets are NOT disjoint
    :return: returns true no elements of set2 are in set1
    """
    for elem in set2:
        if elem in set1:
            raise ValueError(warn)
    return True