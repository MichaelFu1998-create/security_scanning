def matthews_correl_coeff(ntp, ntn, nfp, nfn):
    '''
    This calculates the Matthews correlation coefficent.

    https://en.wikipedia.org/wiki/Matthews_correlation_coefficient

    Parameters
    ----------

    ntp : int
        The number of true positives.

    ntn : int
        The number of true negatives

    nfp : int
        The number of false positives.

    nfn : int
        The number of false negatives.

    Returns
    -------

    float
        The Matthews correlation coefficient.

    '''

    mcc_top = (ntp*ntn - nfp*nfn)
    mcc_bot = msqrt((ntp + nfp)*(ntp + nfn)*(ntn + nfp)*(ntn + nfn))

    if mcc_bot > 0:
        return mcc_top/mcc_bot
    else:
        return np.nan