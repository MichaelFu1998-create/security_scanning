def isarray(array, test, dim=2):
    """Returns True if test is True for all array elements.
    Otherwise, returns False.
    """
    if dim > 1:
        return all(isarray(array[i], test, dim - 1)
                   for i in range(len(array)))
    return all(test(i) for i in array)