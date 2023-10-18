def _autocov(s, **kwargs):
    """Returns the autocovariance of signal s at all lags.

    Adheres to the definition
    sxx[k] = E{S[n]S[n+k]} = cov{S[n],S[n+k]}
    where E{} is the expectation operator, and S is a zero mean process
    """
    # only remove the mean once, if needed
    debias = kwargs.pop('debias', True)
    axis = kwargs.get('axis', -1)
    if debias:
        s = _remove_bias(s, axis)
    kwargs['debias'] = False
    return _crosscov(s, s, **kwargs)