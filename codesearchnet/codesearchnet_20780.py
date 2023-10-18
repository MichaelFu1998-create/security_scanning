def contains_all(set1, set2, warn):
    """
    Checks if all elements from set2 are in set1.

    :param set1:  a set of values
    :param set2:  a set of values
    :param warn: the error message that should be thrown 
     when the sets are not containd
    :return: returns true if all values of set2 are in set1
    """
    for elem in set2:
        if elem not in set1:
            raise ValueError(warn)
    return True