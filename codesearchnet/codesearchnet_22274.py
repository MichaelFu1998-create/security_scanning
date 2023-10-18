def get(f, key, default=None):
    """
    Gets an array from datasets.

    .. versionadded:: 1.4
    """

    if key in f.keys():
        val = f[key].value

        if default is None:
            return val
        else:
            if _np.shape(val) == _np.shape(default):
                return val

    return default