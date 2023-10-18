def min_max(x, na_rm=False, finite=True):
    """
    Return the minimum and maximum of x

    Parameters
    ----------
    x : array_like
        Sequence
    na_rm : bool
        Whether to remove ``nan`` values.
    finite : bool
        Whether to consider only finite values.

    Returns
    -------
    out : tuple
        (minimum, maximum) of x
    """
    if not hasattr(x, 'dtype'):
        x = np.asarray(x)

    if na_rm and finite:
        x = x[np.isfinite(x)]
    elif not na_rm and np.any(np.isnan(x)):
        return np.nan, np.nan
    elif na_rm:
        x = x[~np.isnan(x)]
    elif finite:
        x = x[~np.isinf(x)]

    if (len(x)):
        return np.min(x), np.max(x)
    else:
        return float('-inf'), float('inf')