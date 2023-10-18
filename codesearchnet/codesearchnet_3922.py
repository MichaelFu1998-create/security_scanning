def allsame(iterable, eq=operator.eq):
    """
    Determine if all items in a sequence are the same

    Args:
        iterable (Iterable): items to determine if they are all the same

        eq (Callable, optional): function to determine equality
            (default: operator.eq)

    Example:
        >>> allsame([1, 1, 1, 1])
        True
        >>> allsame([])
        True
        >>> allsame([0, 1])
        False
        >>> iterable = iter([0, 1, 1, 1])
        >>> next(iterable)
        >>> allsame(iterable)
        True
        >>> allsame(range(10))
        False
        >>> allsame(range(10), lambda a, b: True)
        True
    """
    iter_ = iter(iterable)
    try:
        first = next(iter_)
    except StopIteration:
        return True
    return all(eq(first, item) for item in iter_)