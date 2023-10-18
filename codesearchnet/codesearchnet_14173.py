def sort_by_preference(options, prefer):
    """
    :param options: List of options
    :param prefer: Prefered options
    :return:

    Pass in a list of options, return options in 'prefer' first

    >>> sort_by_preference(["cairo", "cairocffi"], ["cairocffi"])
    ["cairocffi", "cairo"]
    """
    if not prefer:
        return options
    return sorted(options, key=lambda x: (prefer + options).index(x))