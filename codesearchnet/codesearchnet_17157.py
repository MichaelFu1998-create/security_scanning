def set_percentage(x: Iterable[X], y: Iterable[X]) -> float:
    """What percentage of x is contained within y?

    :param set x: A set
    :param set y: Another set
    :return: The percentage of x contained within y
    """
    a, b = set(x), set(y)

    if not a:
        return 0.0

    return len(a & b) / len(a)