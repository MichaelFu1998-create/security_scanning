def boxcox_trans(p, **kwargs):
    """
    Boxcox Transformation

    Parameters
    ----------
    p : float
        Power parameter, commonly denoted by
        lower-case lambda in formulae
    kwargs : dict
        Keyword arguments passed onto
        :func:`trans_new`. Should not include
        the `transform` or `inverse`.
    """
    if np.abs(p) < 1e-7:
        return log_trans()

    def transform(x):
        return (x**p - 1) / (p * np.sign(x-1))

    def inverse(x):
        return (np.abs(x) * p + np.sign(x)) ** (1 / p)

    kwargs['p'] = p
    kwargs['name'] = kwargs.get('name', 'pow_{}'.format(p))
    kwargs['transform'] = transform
    kwargs['inverse'] = inverse
    return trans_new(**kwargs)