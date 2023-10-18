def _gaussian(x, amp, loc, std):
    '''This is a simple gaussian.

    Parameters
    ----------

    x : np.array
        The items at which the Gaussian is evaluated.

    amp : float
        The amplitude of the Gaussian.

    loc : float
        The central value of the Gaussian.

    std : float
        The standard deviation of the Gaussian.

    Returns
    -------

    np.array
        Returns the Gaussian evaluated at the items in `x`, using the provided
        parameters of `amp`, `loc`, and `std`.

    '''

    return amp * np.exp(-((x - loc)*(x - loc))/(2.0*std*std))