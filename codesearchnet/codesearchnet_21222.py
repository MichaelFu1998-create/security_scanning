def create_hierarchy(hierarchy, level):
    """Create an OrderedDict

    :param hierarchy: a dictionary
    :param level: single key
    :return: deeper dictionary
    """
    if level not in hierarchy:
        hierarchy[level] = OrderedDict()
    return hierarchy[level]