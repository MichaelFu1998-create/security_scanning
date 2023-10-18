def _autocorr_func3(mags, lag, maglen, magmed, magstd):
    '''
    This is yet another alternative to calculate the autocorrelation.

    Taken from: `Bayesian Methods for Hackers by Cameron Pilon <http://nbviewer.jupyter.org/github/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/blob/master/Chapter3_MCMC/Chapter3.ipynb#Autocorrelation>`_

    (This should be the fastest method to calculate ACFs.)

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

    # from http://tinyurl.com/afz57c4
    result = npcorrelate(mags, mags, mode='full')
    result = result / npmax(result)

    return result[int(result.size / 2):]