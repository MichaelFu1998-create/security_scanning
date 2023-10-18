def smooth_magseries_savgol(mags, windowsize, polyorder=2):
    '''This smooths the magseries with a Savitsky-Golay filter.

    Parameters
    ----------

    mags : np.array
        The input mags/flux time-series to smooth.

    windowsize : int
        This is a odd integer containing the smoothing window size.

    polyorder : int
        This is an integer containing the polynomial degree order to use when
        generating the Savitsky-Golay filter.

    Returns
    -------

    np.array
        The smoothed mag/flux time-series array.

    '''

    smoothed = savgol_filter(mags, windowsize, polyorder)
    return smoothed