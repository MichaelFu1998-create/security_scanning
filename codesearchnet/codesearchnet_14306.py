def exp_trans(base=None, **kwargs):
    """
    Create a exponential transform class for *base*

    This is inverse of the log transform.

    Parameters
    ----------
    base : float
        Base of the logarithm
    kwargs : dict
        Keyword arguments passed onto
        :func:`trans_new`. Should not include
        the `transform` or `inverse`.

    Returns
    -------
    out : type
        Exponential transform class
    """
    # default to e
    if base is None:
        name = 'power_e'
        base = np.exp(1)
    else:
        name = 'power_{}'.format(base)

    # transform function
    def transform(x):
        return base ** x

    # inverse function
    def inverse(x):
        return np.log(x)/np.log(base)

    kwargs['base'] = base
    return trans_new(name, transform, inverse, **kwargs)