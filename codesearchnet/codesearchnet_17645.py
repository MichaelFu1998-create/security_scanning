def count_with_multiplier(groups, multiplier):
    """ Update group counts with multiplier

    This is for handling atom counts on groups like (OH)2

    :param groups: iterable of Group/Element
    :param multiplier: the number to multiply by

    """
    counts = collections.defaultdict(float)
    for group in groups:
        for element, count in group.count().items():
            counts[element] += count*multiplier
    return counts