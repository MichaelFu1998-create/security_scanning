def _autocorr_func1(mags, lag, maglen, magmed, magstd):
    '''Calculates the autocorr of mag series for specific lag.

    This version of the function is taken from: Kim et al. (`2011
    <https://dx.doi.org/10.1088/0004-637X/735/2/68>`_)

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

    lagindex = nparange(1,maglen-lag)
    products = (mags[lagindex] - magmed) * (mags[lagindex+lag] - magmed)
    acorr = (1.0/((maglen - lag)*magstd)) * npsum(products)

    return acorr