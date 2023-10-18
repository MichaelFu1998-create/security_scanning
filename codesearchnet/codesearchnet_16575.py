def aggregate(l):
    """Aggregate a `list` of prefixes.

    Keyword arguments:
    l -- a python list of prefixes

    Example use:
    >>> aggregate(["10.0.0.0/8", "10.0.0.0/24"])
    ['10.0.0.0/8']
    """
    tree = radix.Radix()
    for item in l:
        try:
            tree.add(item)
        except (ValueError) as err:
            raise Exception("ERROR: invalid IP prefix: {}".format(item))

    return aggregate_tree(tree).prefixes()