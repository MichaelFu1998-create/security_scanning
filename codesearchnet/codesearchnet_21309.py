def f_hierarchical_passages(reffs, citation):
    """ A function to construct a hierarchical dictionary representing the different citation layers of a text

    :param reffs: passage references with human-readable equivalent
    :type reffs: [(str, str)]
    :param citation: Main Citation
    :type citation: Citation
    :return: nested dictionary representing where keys represent the names of the levels and the final values represent the passage reference
    :rtype: OrderedDict
    """
    d = OrderedDict()
    levels = [x for x in citation]
    for cit, name in reffs:
        ref = cit.split('-')[0]
        levs = ['%{}|{}%'.format(levels[i].name, v) for i, v in enumerate(ref.split('.'))]
        getFromDict(d, levs[:-1])[name] = cit
    return d