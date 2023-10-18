def is_close_to_int(x):
    """
    Check if value is close to an integer

    Parameters
    ----------
    x : float
        Numeric value to check

    Returns
    -------
    out : bool
    """
    if not np.isfinite(x):
        return False
    return abs(x - nearest_int(x)) < 1e-10