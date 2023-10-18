def _smooth_acf_savgol(acf, windowsize=21, polyorder=2):
    '''
    This returns a smoothed version of the ACF.

    This version uses the Savitsky-Golay smoothing filter.

    Parameters
    ----------

    acf : np.array
        The auto-correlation function array to smooth.

    windowsize : int
        The number of input points to apply the smoothing over.

    polyorder : int
        The order of the polynomial to use in the Savitsky-Golay filter.

    Returns
    -------

    np.array
        Smoothed version of the input ACF array.

    '''

    smoothed = savgol_filter(acf, windowsize, polyorder)

    return smoothed