def filter_symlog(y, base=10.0):
    """Symmetrical logarithmic scale.

    Optional arguments:

    *base*:
        The base of the logarithm.
    """
    log_base = np.log(base)
    sign = np.sign(y)
    logs = np.log(np.abs(y) / log_base)
    return sign * logs