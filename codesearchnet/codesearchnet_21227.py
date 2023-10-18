def level_grouper(text, getreffs, level=None, groupby=20):
    """ Alternative to level_chunker: groups levels together at the latest level

    :param text: Text object
    :param getreffs: GetValidReff query callback
    :param level: Level of citation to retrieve
    :param groupby: Number of level to groupby
    :return: Automatically curated references
    """
    if level is None or level > len(text.citation):
        level = len(text.citation)

    references = [ref.split(":")[-1] for ref in getreffs(level=level)]
    _refs = OrderedDict()

    for key in references:
        k = ".".join(key.split(".")[:level-1])
        if k not in _refs:
            _refs[k] = []
        _refs[k].append(key)
        del k

    return [
        (
            join_or_single(ref[0], ref[-1]),
            join_or_single(ref[0], ref[-1])
        )
        for sublist in _refs.values()
        for ref in [
            sublist[i:i+groupby]
            for i in range(0, len(sublist), groupby)
        ]
    ]