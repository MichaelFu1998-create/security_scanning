def get_subdict(adict, path, sep=os.sep):
    """
    Given a nested dictionary adict.
    This returns its childen just below the path.
    The path is a string composed of adict keys separated by sep.

    :param adict: nested dict

    :param path: str

    :param sep: str

    :return: dict or list or leaf of treemap

    """
    return reduce(adict.__class__.get, [p for p in op.split(sep) if p], adict)