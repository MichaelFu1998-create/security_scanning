def _autocorr_func2(mags, lag, maglen, magmed, magstd):
    '''
    This is an alternative function to calculate the autocorrelation.

    This version is from (first definition):

    https://en.wikipedia.org/wiki/Correlogram#Estimation_of_autocorrelations

    Parameters
    ----------

    mags : np.array
        This is the magnitudes array. MUST NOT have any nans.

    lag : float
        The specific lag value to calculate the auto-correlation for. This MUST
        be less than total number of observations in `mags`.

    maglen : int
        The number of elements in the `mags` array.

    magmed : float
        The median of the `mags` array.

    magstd : float
        The standard deviation of the `mags` array.

    Returns
    -------

    float
        The auto-correlation at this specific `lag` value.

    '''

    lagindex = nparange(0,maglen-lag)
    products = (mags[lagindex] - magmed) * (mags[lagindex+lag] - magmed)

    autocovarfunc = npsum(products)/lagindex.size
    varfunc = npsum(
        (mags[lagindex] - magmed)*(mags[lagindex] - magmed)
    )/mags.size

    acorr = autocovarfunc/varfunc

    return acorr