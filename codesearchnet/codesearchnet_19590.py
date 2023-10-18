def findfolder(toppath, match='*', exclude=''):
    """
    recursively find folder path from toppath.
    patterns to decide to walk folder path or not
    :type toppath: str
    :type match: str or list(str)
    :type exclude: str or list(str)
    :rtype: generator for path str
    """
    pred = _pred_pattern(match, exclude)

    return (p for p in walkfolder(toppath, pred))