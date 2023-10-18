def aggregated(cache=DEFAULT_CACHE):
    """
    A dictionary of all aggregated words.

    They keys in the dictionary correspond to subfolders in the aggregated cache.
    Each key has a list of words. Each of these words is the name of an XML-file
    in the subfolder. The XML-file contains color information harvested from the web
    (or handmade).
    """
    global _aggregated_name, _aggregated_dict
    if _aggregated_name != cache:
        _aggregated_name = cache
        _aggregated_dict = {}
        for path in glob(os.path.join(cache, "*")):
            if os.path.isdir(path):
                p = os.path.basename(path)
                _aggregated_dict[p] = glob(os.path.join(path, "*"))
                _aggregated_dict[p] = [os.path.basename(f)[:-4] for f in _aggregated_dict[p]]

    return _aggregated_dict