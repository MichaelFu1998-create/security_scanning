def precision(ntp, nfp):
    '''
    This calculates precision.

    https://en.wikipedia.org/wiki/Precision_and_recall

    Parameters
    ----------

    ntp : int
        The number of true positives.

    nfp : int
        The number of false positives.

    Returns
    -------

    float
        The precision calculated using `ntp/(ntp + nfp)`.

    '''

    if (ntp+nfp) > 0:
        return ntp/(ntp+nfp)
    else:
        return np.nan