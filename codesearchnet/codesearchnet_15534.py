def pairwise(lst):
    """ yield item i and item i+1 in lst. e.g.
        (lst[0], lst[1]), (lst[1], lst[2]), ..., (lst[-1], None)
    Args:
        lst (list): List to process
    Returns:
        list
    """
    if not lst:
        return
    length = len(lst)
    for i in range(length - 1):
        yield lst[i], lst[i + 1]
    yield lst[-1], None