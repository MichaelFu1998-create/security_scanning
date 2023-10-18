def probability_trans(distribution, *args, **kwargs):
    """
    Probability Transformation

    Parameters
    ----------
    distribution : str
        Name of the distribution. Valid distributions are
        listed at :mod:`scipy.stats`. Any of the continuous
        or discrete distributions.
    args : tuple
        Arguments passed to the distribution functions.
    kwargs : dict
        Keyword arguments passed to the distribution functions.

    Notes
    -----
    Make sure that the distribution is a good enough
    approximation for the data. When this is not the case,
    computations may run into errors. Absence of any errors
    does not imply that the distribution fits the data.
    """
    import scipy.stats as stats
    cdists = {k for k in dir(stats)
              if hasattr(getattr(stats, k), 'cdf')}
    if distribution not in cdists:
        msg = "Unknown distribution '{}'"
        raise ValueError(msg.format(distribution))

    try:
        doc = kwargs.pop('_doc')
    except KeyError:
        doc = ''

    try:
        name = kwargs.pop('_name')
    except KeyError:
        name = 'prob_{}'.format(distribution)

    def transform(x):
        return getattr(stats, distribution).cdf(x, *args, **kwargs)

    def inverse(x):
        return getattr(stats, distribution).ppf(x, *args, **kwargs)

    return trans_new(name,
                     transform, inverse, domain=(0, 1),
                     doc=doc)