def ViswanathNatarajan3(T, A, B, C):
    r'''Calculate the viscosity of a liquid using the 3-term Antoine form
    representation developed in [1]_. Requires input coefficients. The `A`
    coefficient is assumed to yield coefficients in centipoise, as all 
    coefficients found so far have been.

    .. math::
        \log_{10} \mu = A + B/(T + C)

    Parameters
    ----------
    T : float
        Temperature of fluid [K]

    Returns
    -------
    mu : float
        Liquid viscosity, [Pa*s]

    Notes
    -----
    No other source for these coefficients has been found.

    Examples
    --------
    >>> ViswanathNatarajan3(298.15, -2.7173, -1071.18, -129.51)
    0.0006129806445142112

    References
    ----------
    .. [1] Viswanath, Dabir S., and G. Natarajan. Databook On The Viscosity Of
       Liquids. New York: Taylor & Francis, 1989
    '''
    mu = 10**(A + B/(C - T))
    return mu/1000.