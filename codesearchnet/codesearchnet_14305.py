def log_trans(base=None, **kwargs):
    """
    Create a log transform class for *base*

    Parameters
    ----------
    base : float
        Base for the logarithm. If None, then
        the natural log is used.
    kwargs : dict
        Keyword arguments passed onto
        :func:`trans_new`. Should not include
        the `transform` or `inverse`.

    Returns
    -------
    out : type
        Log transform class
    """
    # transform function
    if base is None:
        name = 'log'
        base = np.exp(1)
        transform = np.log
    elif base == 10:
        name = 'log10'
        transform = np.log10
    elif base == 2:
        name = 'log2'
        transform = np.log2
    else:
        name = 'log{}'.format(base)

        def transform(x):
            return np.log(x)/np.log(base)

    # inverse function
    def inverse(x):
        try:
            return base ** x
        except TypeError:
            return [base**val for val in x]

    if 'domain' not in kwargs:
        kwargs['domain'] = (sys.float_info.min, np.inf)

    if 'breaks' not in kwargs:
        kwargs['breaks'] = log_breaks(base=base)

    kwargs['base'] = base
    kwargs['_format'] = log_format(base)

    _trans = trans_new(name, transform, inverse, **kwargs)

    if 'minor_breaks' not in kwargs:
        n = int(base) - 2
        _trans.minor_breaks = trans_minor_breaks(_trans, n=n)

    return _trans