def is_single_float(val):
    """
    Checks whether a variable is a float.

    Parameters
    ----------
    val
        The variable to check.

    Returns
    -------
    bool
        True if the variable is a float. Otherwise False.

    """
    return isinstance(val, numbers.Real) and not is_single_integer(val) and not isinstance(val, bool)