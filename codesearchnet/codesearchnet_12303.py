def recall(ntp, nfn):
    '''
    This calculates recall.

    https://en.wikipedia.org/wiki/Precision_and_recall

    Parameters
    ----------

    ntp : int
        The number of true positives.

    nfn : int
        The number of false negatives.

    Returns
    -------

    float
        The precision calculated using `ntp/(ntp + nfn)`.

    '''

    if (ntp+nfn) > 0:
        return ntp/(ntp+nfn)
    else:
        return np.nan