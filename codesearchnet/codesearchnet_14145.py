def sorted(list, cmp=None, reversed=False):
    """ Returns a sorted copy of the list.
    """
    list = [x for x in list]
    list.sort(cmp)
    if reversed: list.reverse()
    return list