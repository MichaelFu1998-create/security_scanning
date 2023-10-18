def MatchMasks(filename, masks):
    '''
    Verifies if a filename match with given patterns.

    :param str filename: The filename to match.
    :param list(str) masks: The patterns to search in the filename.
    :return bool:
        True if the filename has matched with one pattern, False otherwise.
    '''
    import fnmatch

    if not isinstance(masks, (list, tuple)):
        masks = [masks]

    for i_mask in masks:
        if fnmatch.fnmatch(filename, i_mask):
            return True
    return False