def _double_inverted_gaussian(x,
                              amp1, loc1, std1,
                              amp2, loc2, std2):
    '''This is a double inverted gaussian.

    Parameters
    ----------

    x : np.array
        The items at which the Gaussian is evaluated.

    amp1,amp2 : float
        The amplitude of Gaussian 1 and Gaussian 2.

    loc1,loc2 : float
        The central value of Gaussian 1 and Gaussian 2.

    std1,std2 : float
        The standard deviation of Gaussian 1 and Gaussian 2.

    Returns
    -------

    np.array
        Returns a double inverted Gaussian function evaluated at the items in
        `x`, using the provided parameters of `amp`, `loc`, and `std` for two
        component Gaussians 1 and 2.

    '''

    gaussian1 = -_gaussian(x,amp1,loc1,std1)
    gaussian2 = -_gaussian(x,amp2,loc2,std2)
    return gaussian1 + gaussian2